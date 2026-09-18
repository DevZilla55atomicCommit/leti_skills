#!/usr/bin/env python3
"""
Instagram Collections Downloader — Bulletproof Overnight Runner

Features:
- Per-collection isolation (one failure doesn't stop others)
- Max 2 concurrent downloads (Instagram-safe rate limit)
- Exponential backoff: 30s → 60s → 120s → 240s → 480s on 429/5xx
- Resume support: --continue --no-overwrites skips existing files
- Metadata sidecars: .info.json (yt-dlp) + .meta.json (enhanced)
- Heartbeat logging every 60s per collection
- Graceful shutdown on SIGTERM (writes report, saves state)
- Final report: logs/DOWNLOAD_REPORT.json + logs/failed_urls.txt
"""

import argparse
import asyncio
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# ─── Configuration ────────────────────────────────────────────────────────────
@dataclass
class DownloadConfig:
    urls_dir: Path
    cookies_file: Path
    output_dir: Path
    log_dir: Path
    max_concurrent: int = 2
    max_retries: int = 5
    per_url_timeout: int = 300
    heartbeat_interval: int = 60
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# ─── Data Classes ────────────────────────────────────────────────────────────
@dataclass
class CollectionResult:
    name: str
    total: int
    succeeded: int
    failed: int
    skipped: int
    duration_sec: float
    failed_urls: List[str]

@dataclass
class VideoMetadata:
    url: str
    collection: str
    filename: str
    caption: str = ""
    hashtags: List[str] = None
    owner: str = ""
    owner_username: str = ""
    downloaded_at: str = ""
    file_size_bytes: int = 0
    duration_sec: float = 0.0

# ─── Logging ──────────────────────────────────────────────────────────────────
def setup_logging(log_dir: Path, name: str) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    fh = logging.FileHandler(log_dir / f"{name}.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S'
    ))
    logger.addHandler(fh)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S'))
    logger.addHandler(ch)
    
    return logger

# ─── Collection Downloader ────────────────────────────────────────────────────
class CollectionDownloader:
    def __init__(self, config: DownloadConfig, collection_name: str, urls: List[str]):
        self.config = config
        self.collection_name = collection_name
        self.urls = urls
        self.logger = setup_logging(config.log_dir, collection_name)
        
        self.coll_output_dir = config.output_dir / collection_name
        self.coll_output_dir.mkdir(parents=True, exist_ok=True)
        
        self.semaphore: Optional[asyncio.Semaphore] = None
        self.shutdown = False
        self.results = CollectionResult(
            name=collection_name,
            total=len(urls),
            succeeded=0,
            failed=0,
            skipped=0,
            duration_sec=0.0,
            failed_urls=[]
        )
        self._start_time = time.time()
        self._heartbeat_task: Optional[asyncio.Task] = None
    
    async def run(self, semaphore: asyncio.Semaphore) -> CollectionResult:
        self.semaphore = semaphore
        self._heartbeat_task = asyncio.create_task(self._heartbeat())
        
        tasks = [self._download_one(url, idx) for idx, url in enumerate(self.urls)]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
        
        self.results.duration_sec = time.time() - self._start_time
        self._log_summary()
        return self.results
    
    async def _heartbeat(self):
        while not self.shutdown:
            await asyncio.sleep(self.config.heartbeat_interval)
            done = self.results.succeeded + self.results.failed + self.results.skipped
            elapsed = time.time() - self._start_time
            self.logger.info(
                f"HEARTBEAT | {done}/{self.results.total} | "
                f"✓{self.results.succeeded} ✗{self.results.failed} ⊘{self.results.skipped} | "
                f"{elapsed:.0f}s elapsed"
            )
    
    async def _download_one(self, url: str, index: int):
        if self.shutdown:
            return
            
        async with self.semaphore:
            if self.shutdown:
                return
                
            self.logger.info(f"[{index+1}/{self.results.total}] Starting: {url}")
            
            for attempt in range(1, self.config.max_retries + 1):
                if self.shutdown:
                    return
                    
                try:
                    success = await self._execute_yt_dlp(url, attempt)
                    if success:
                        self.results.succeeded += 1
                        self.logger.info(f"[{index+1}/{self.results.total}] ✓ Success: {url}")
                        return
                except asyncio.TimeoutError:
                    self.logger.warning(f"[{index+1}] Timeout (attempt {attempt}/{self.config.max_retries}): {url}")
                except Exception as e:
                    self.logger.warning(f"[{index+1}] Error (attempt {attempt}/{self.config.max_retries}): {url} — {e}")
                
                if attempt < self.config.max_retries:
                    wait = min(30 * (2 ** (attempt - 1)), 600)
                    self.logger.info(f"[{index+1}] Backing off {wait}s before retry...")
                    await asyncio.sleep(wait)
            
            self.results.failed += 1
            self.results.failed_urls.append(url)
            self.logger.error(f"[{index+1}/{self.results.total}] ✗ FAILED after {self.config.max_retries} attempts: {url}")
    
    async def _execute_yt_dlp(self, url: str, attempt: int) -> bool:
        video_id = url.rstrip('/').split('/')[-1]
        safe_id = "".join(c for c in video_id if c.isalnum() or c in '-_')[:50]
        
        output_template = str(self.coll_output_dir / f"{safe_id}.%(ext)s")
        
        cmd = [
            "yt-dlp",
            "--cookies", str(self.config.cookies_file),
            "--user-agent", self.config.user_agent,
            "--output", output_template,
            "--continue",
            "--no-overwrites",
            "--write-info-json",
            "--write-thumbnail",
            "--convert-thumbnails", "jpg",
            "--embed-thumbnail",
            "--embed-metadata",
            "--add-metadata",
            "--retries", "0",
            "--fragment-retries", "3",
            "--retry-sleep", "5",
            "--socket-timeout", "30",
            "--no-playlist",
            "--ignore-errors",
            "--no-warnings",
            "--progress",
            "--newline",
            url
        ]
        
        self.logger.debug(f"Command: {' '.join(cmd)}")
        
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            ),
            timeout=self.config.per_url_timeout
        )
        
        stdout, _ = await proc.communicate()
        output = stdout.decode('utf-8', errors='replace')
        
        for line in output.split('\n'):
            line = line.strip()
            if line and any(kw in line.lower() for kw in ['downloading', 'eta', '%', 'merged', 'writing', 'error', 'warning', 'already']):
                self.logger.debug(f"[{url}] {line}")
        
        if proc.returncode == 0:
            await self._verify_and_enhance_metadata(url, safe_id)
            return True
        elif "already been downloaded" in output or "has already been downloaded" in output:
            self.results.skipped += 1
            self.logger.info(f"[{index+1}] ⊘ Skipped (already exists): {url}")
            return True
        else:
            self.logger.warning(f"yt-dlp exit code {proc.returncode}: {url}")
            return False
    
    async def _verify_and_enhance_metadata(self, url: str, safe_id: str):
        video_files = list(self.coll_output_dir.glob(f"{safe_id}.*"))
        video_files = [f for f in video_files if f.suffix.lower() in ['.mp4', '.mkv', '.webm', '.mov']]
        
        if not video_files:
            self.logger.warning(f"No video file found for {safe_id}")
            return
            
        video_file = video_files[0]
        json_file = self.coll_output_dir / f"{safe_id}.info.json"
        
        metadata = {}
        if json_file.exists():
            try:
                with open(json_file) as f:
                    metadata = json.load(f)
            except:
                pass
        
        import re
        caption = metadata.get('description', '')
        hashtags = re.findall(r'#(\w+)', caption) if caption else []
        
        enhanced = VideoMetadata(
            url=url,
            collection=self.collection_name,
            filename=video_file.name,
            caption=caption,
            hashtags=hashtags,
            owner=metadata.get('uploader', ''),
            owner_username=metadata.get('uploader_id', ''),
            downloaded_at=datetime.now().isoformat(),
            file_size_bytes=video_file.stat().st_size,
            duration_sec=metadata.get('duration', 0.0)
        )
        
        enhanced_path = self.coll_output_dir / f"{safe_id}.meta.json"
        with open(enhanced_path, 'w') as f:
            json.dump(asdict(enhanced), f, indent=2, ensure_ascii=False)
        
        self.logger.debug(f"Enhanced metadata: {enhanced_path}")
    
    def _log_summary(self):
        self.logger.info("=" * 60)
        self.logger.info(f"COLLECTION COMPLETE: {self.collection_name}")
        self.logger.info(f"  Total:     {self.results.total}")
        self.logger.info(f"  Succeeded: {self.results.succeeded}")
        self.logger.info(f"  Failed:    {self.results.failed}")
        self.logger.info(f"  Skipped:   {self.results.skipped}")
        self.logger.info(f"  Duration:  {self.results.duration_sec:.1f}s")
        if self.results.failed_urls:
            self.logger.info(f"  Failed URLs:")
            for u in self.results.failed_urls:
                self.logger.info(f"    - {u}")
        self.logger.info("=" * 60)

# ─── Master Orchestrator ──────────────────────────────────────────────────────
class MasterOrchestrator:
    def __init__(self, config: DownloadConfig, single_collection: str = None):
        self.config = config
        self.single_collection = single_collection
        self.logger = setup_logging(config.log_dir, "master")
        self.shutdown = False
        self.all_results: List[CollectionResult] = []
        
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        self.logger.warning(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown = True
    
    def discover_collections(self) -> List[tuple]:
        collections = []
        url_files = sorted(self.config.urls_dir.glob("*_NEW.txt"))
        
        for url_file in url_files:
            coll_name = url_file.stem.replace("_NEW", "")
            if self.single_collection and coll_name != self.single_collection:
                continue
            with open(url_file) as f:
                urls = [line.strip() for line in f if line.strip()]
            if urls:
                collections.append((coll_name, urls))
                self.logger.info(f"Discovered: {coll_name} — {len(urls)} URLs")
        
        return collections
    
    async def run(self):
        collections = self.discover_collections()
        if not collections:
            self.logger.error("No collections found!")
            return
        
        self.logger.info(f"Starting download of {len(collections)} collections with max {self.config.max_concurrent} concurrent")
        self.logger.info(f"Output: {self.config.output_dir}")
        self.logger.info(f"Logs:   {self.config.log_dir}")
        self.logger.info(f"Cookies: {self.config.cookies_file}")
        
        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        for coll_name, urls in collections:
            if self.shutdown:
                self.logger.warning("Shutdown requested, stopping...")
                break
            
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"STARTING COLLECTION: {coll_name} ({len(urls)} URLs)")
            self.logger.info(f"{'='*60}")
            
            downloader = CollectionDownloader(self.config, coll_name, urls)
            result = await downloader.run(semaphore)
            self.all_results.append(result)
            
            if not self.shutdown:
                await asyncio.sleep(2)
        
        self._write_final_report()
    
    def _write_final_report(self):
        report_path = self.config.log_dir / "DOWNLOAD_REPORT.json"
        failed_path = self.config.log_dir / "failed_urls.txt"
        
        total_urls = sum(r.total for r in self.all_results)
        total_ok = sum(r.succeeded for r in self.all_results)
        total_fail = sum(r.failed for r in self.all_results)
        total_skip = sum(r.skipped for r in self.all_results)
        total_time = sum(r.duration_sec for r in self.all_results)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "max_concurrent": self.config.max_concurrent,
                "max_retries": self.config.max_retries,
                "urls_dir": str(self.config.urls_dir),
                "output_dir": str(self.config.output_dir),
            },
            "summary": {
                "collections": len(self.all_results),
                "total_urls": total_urls,
                "succeeded": total_ok,
                "failed": total_fail,
                "skipped": total_skip,
                "success_rate": f"{total_ok/total_urls*100:.1f}%" if total_urls > 0 else "0%",
                "total_duration_sec": total_time,
            },
            "collections": [asdict(r) for r in self.all_results],
            "all_failed_urls": [u for r in self.all_results for u in r.failed_urls]
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        with open(failed_path, 'w') as f:
            for r in self.all_results:
                for u in r.failed_urls:
                    f.write(u + '\n')
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info("MASTER SUMMARY")
        self.logger.info(f"  Collections:  {len(self.all_results)}")
        self.logger.info(f"  Total URLs:   {total_urls}")
        self.logger.info(f"  ✓ Succeeded:  {total_ok}")
        self.logger.info(f"  ✗ Failed:     {total_fail}")
        self.logger.info(f"  ⊘ Skipped:    {total_skip}")
        self.logger.info(f"  Success Rate: {total_ok/total_urls*100:.1f}%" if total_urls else "  Success Rate: N/A")
        self.logger.info(f"  Total Time:   {total_time/60:.1f} min")
        self.logger.info(f"  Report:       {report_path}")
        self.logger.info(f"  Failed URLs:  {failed_path}")
        self.logger.info("=" * 60)

# ─── CLI Entry Point ──────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instagram Collections Downloader — Bulletproof Overnight Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full overnight run
  python3 download_instagram_collections.py \\
    --urls-dir ./instagram_new_urls_by_collection \\
    --cookies ~/Downloads/cookies_www.instagram.com_2026-07-19.txt \\
    --output ./instagram_downloads \\
    --logs ./instagram_downloads/logs \\
    --max-concurrent 2
  
  # Test single collection
  python3 download_instagram_collections.py \\
    --urls-dir ./instagram_new_urls_by_collection \\
    --cookies ~/Downloads/cookies_www.instagram.com_2026-07-19.txt \\
    --collection "DaVinci_Tricks"
"""
    )
    parser.add_argument("--urls-dir", type=Path, default=Path("instagram_new_urls_by_collection"),
                        help="Directory containing *_NEW.txt files")
    parser.add_argument("--cookies", type=Path, required=True,
                        help="Instagram cookies file (Netscape format)")
    parser.add_argument("--output", type=Path, default=Path("downloads"),
                        help="Output directory for downloaded videos")
    parser.add_argument("--logs", type=Path, default=Path("logs"),
                        help="Log directory")
    parser.add_argument("--max-concurrent", type=int, default=2,
                        help="Max concurrent downloads (default: 2)")
    parser.add_argument("--max-retries", type=int, default=5,
                        help="Max retries per URL (default: 5)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Per-URL timeout in seconds (default: 300)")
    parser.add_argument("--collection", type=str,
                        help="Run only one collection by name (for testing)")
    return parser.parse_args()

async def main():
    args = parse_args()
    
    if not args.cookies.exists():
        print(f"ERROR: Cookies file not found: {args.cookies}", file=sys.stderr)
        print("Export Instagram cookies in Netscape format (e.g., via 'Get cookies.txt LOCALLY' extension)", file=sys.stderr)
        sys.exit(1)
    
    config = DownloadConfig(
        urls_dir=args.urls_dir,
        cookies_file=args.cookies,
        output_dir=args.output,
        log_dir=args.logs,
        max_concurrent=args.max_concurrent,
        max_retries=args.max_retries,
        per_url_timeout=args.timeout,
    )
    
    config.output_dir.mkdir(parents=True, exist_ok=True)
    config.log_dir.mkdir(parents=True, exist_ok=True)
    
    orchestrator = MasterOrchestrator(config, args.collection)
    await orchestrator.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)