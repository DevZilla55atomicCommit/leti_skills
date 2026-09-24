#!/usr/bin/env python3
"""
Standalone Instagram Reel Frame Capture Script
Runs via Hermes venv Python (with fixed greenlet)
Uses Playwright async API with injected cookies from Netscape format file

Usage:
    python3 capture_reel_frames.py <reel_url> <cookies_file> <output_dir> [--percentages 0,14,28,42,57,71,86,99.9]
    
Example:
    python3 capture_reel_frames.py \
        "https://www.instagram.com/reel/DZ95PwrBsCQ/" \
        "/Users/alfredkamisese/Downloads/cookies_www.instagram.com_2026-07-19.txt" \
        "/tmp/output_DZ95PwrBsCQ"
"""

import asyncio
import json
import base64
import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


def parse_cookies(netscape_path: str) -> List[Dict[str, Any]]:
    """Parse Netscape format cookies.txt into Playwright cookie list"""
    cookies = []
    with open(netscape_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) >= 7:
                domain, flag, path, secure, expiry, name, value = parts[:7]
                cookies.append({
                    'name': name,
                    'value': value,
                    'domain': domain.lstrip('.'),
                    'path': path,
                    'secure': secure == 'TRUE',
                    'expires': int(expiry) if expiry.isdigit() else -1,
                    'sameSite': 'Lax'
                })
    return cookies


async def extract_metadata(page) -> Dict[str, Any]:
    """Extract reel metadata from the page"""
    metadata = {}
    
    try:
        # Get creator from profile link - try multiple strategies
        profile_selectors = [
            'article header a[href^="/"]:not([href*="/reel/"]):not([href*="/p/"]):not([href*="/tv/"])',
            'header a[href^="/"]:not([href*="/reel/"]):not([href*="/p/"]):not([href*="/tv/"])',
            'a[href^="/"][role="link"]:not([href*="/reel/"]):not([href*="/p/"]):not([href*="/tv/"]):not([href*="/explore"]):not([href*="/stories"])',
            'article [data-testid="post-header"] a[href^="/"]',
        ]
        
        for selector in profile_selectors:
            try:
                elements = await page.query_selector_all(selector)
                for el in elements:
                    href = await el.get_attribute('href')
                    text = await el.text_content()
                    if href and '/' in href and text:
                        parts = [p for p in href.strip('/').split('/') if p]
                        if parts:
                            candidate = parts[0]
                            if candidate not in ['reel', 'p', 'tv', 'explore', 'stories', 'reels', 'accounts', 'accounts_edit', 'direct', 'saved', 'settings']:
                                metadata['creator'] = candidate
                                break
                if metadata.get('creator'):
                    break
            except:
                pass
            if metadata.get('creator'):
                break
        
        # Strategy 2: If still no creator, extract from page title
        if not metadata.get('creator'):
            try:
                title = await page.title()
                if ' • Instagram' in title:
                    metadata['creator'] = title.replace(' • Instagram', '').strip()
                elif '@' in title:
                    metadata['creator'] = title.split('@')[1].split(' ')[0].strip()
            except:
                pass
        
        # Try to get caption/description
        caption_selectors = [
            'article h1',
            'article [data-testid="post-comment-root"]',
            'meta[property="og:description"]',
            'meta[name="description"]',
            'header + div div span',
        ]
        
        for selector in caption_selectors:
            el = await page.query_selector(selector)
            if el:
                text = await el.get_attribute('content') or await el.text_content()
                if text and len(text) > 20:
                    metadata['caption'] = text.strip()[:2000]
                    break
        
        # Get hashtags from caption
        if 'caption' in metadata:
            metadata['hashtags'] = re.findall(r'#(\w+)', metadata['caption'])
        
        # Try to get engagement metrics
        engagement_selectors = {
            'likes': ['button:has-text("likes")', 'button:has-text("like")', '[aria-label*="like"]'],
            'comments': ['button:has-text("comments")', 'button:has-text("Comment")'],
        }
        
        for key, selectors in engagement_selectors.items():
            for selector in selectors:
                try:
                    el = await page.query_selector(selector)
                    if el:
                        text = await el.text_content()
                        if text:
                            metadata[key] = text.strip()
                            break
                except:
                    pass
        
        # Get upload date from time element
        time_el = await page.query_selector('time[datetime]')
        if time_el:
            datetime_attr = await time_el.get_attribute('datetime')
            if datetime_attr:
                metadata['upload_date'] = datetime_attr
        
    except Exception as e:
        print(f"  ⚠️  Metadata extraction partial: {e}")
    
    return metadata


async def capture_frames(url: str, cookies_file: str, output_dir: str, 
                        percentages: Optional[List[float]] = None) -> Dict[str, Any]:
    """Capture frames from Instagram reel at specified percentages"""
    if percentages is None:
        percentages = [0, 14, 28, 42, 57, 71, 86, 99.9]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    frames_dir = output_path / 'frames'
    frames_dir.mkdir(exist_ok=True)

    cookies = parse_cookies(cookies_file)
    print(f"Loaded {len(cookies)} cookies from {cookies_file}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies(cookies)

        page = await context.new_page()

        print(f"Navigating to {url}...")
        await page.goto(url, wait_until='networkidle', timeout=30000)

        # Wait for video element
        await page.wait_for_selector('video', timeout=10000)
        await page.wait_for_timeout(2000)  # Let video buffer

        # Extract metadata
        print("Extracting metadata...")
        metadata = await extract_metadata(page)

        # Get video info
        video_info = await page.evaluate("""
            () => {
                const v = document.querySelector('video');
                return v ? {
                    duration: v.duration,
                    videoWidth: v.videoWidth,
                    videoHeight: v.videoHeight,
                    src: v.currentSrc
                } : null;
            }
        """)

        if not video_info or not video_info['duration']:
            await browser.close()
            raise Exception("Could not find video or get duration")

        duration = video_info['duration']
        print(f"Video duration: {duration:.2f}s, size: {video_info['videoWidth']}x{video_info['videoHeight']}")

        frames_captured = []

        for i, pct in enumerate(percentages):
            target_time = (pct / 100) * duration
            # Cap at 99.9% to avoid seeking past end
            if target_time >= duration:
                target_time = duration * 0.999

            print(f"  Capturing frame {i+1}/{len(percentages)} at {pct}% ({target_time:.2f}s)...")

            # Seek and wait for seeked event
            await page.evaluate(f"""
                (async () => {{
                    const v = document.querySelector('video');
                    v.currentTime = {target_time};
                    await new Promise(r => {{
                        v.onseeked = () => r();
                        setTimeout(r, 3000);
                    }});
                    await new Promise(r => setTimeout(r, 300));
                }})()
            """)

            # Capture frame via canvas
            data_url = await page.evaluate("""
                () => {
                    const v = document.querySelector('video');
                    const canvas = document.createElement('canvas');
                    canvas.width = v.videoWidth;
                    canvas.height = v.videoHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(v, 0, 0);
                    return canvas.toDataURL('image/png');
                }
            """)

            if data_url and data_url.startswith('data:image/png;base64,'):
                b64_data = data_url.split(',')[1]
                b64_data += '=' * ((4 - len(b64_data) % 4) % 4)
                img_data = base64.b64decode(b64_data)

                frame_filename = f'frame_{i:02d}.png'
                frame_path = frames_dir / frame_filename
                with open(frame_path, 'wb') as f:
                    f.write(img_data)

                frames_captured.append({
                    'index': i,
                    'percent': pct,
                    'time': round(target_time, 2),
                    'filename': frame_filename,
                    'path': str(frame_path),
                    'size': len(img_data)
                })
                print(f"    Saved {frame_filename} ({len(img_data)} bytes)")
            else:
                print(f"    FAILED to capture frame {i}")

        await browser.close()

    return {
        'url': url,
        'duration': round(duration, 2),
        'video_width': video_info['videoWidth'],
        'video_height': video_info['videoHeight'],
        'frames': frames_captured,
        'frames_dir': str(frames_dir),
        'metadata': metadata
    }


def create_gif(frames_dir: str, output_path: str, fps: int = 2) -> bool:
    """Create GIF from frames using ffmpeg"""
    frame_pattern = os.path.join(frames_dir, 'frame_%02d.png')
    palette_path = os.path.join(frames_dir, 'palette.png')

    # Generate palette
    cmd1 = [
        'ffmpeg', '-y', '-framerate', str(fps),
        '-i', frame_pattern,
        '-vf', 'scale=720:-1:flags=lanczos,palettegen=stats_mode=diff',
        palette_path
    ]
    result = subprocess.run(cmd1, capture_output=True)
    if result.returncode != 0:
        print(f"Palette generation failed: {result.stderr.decode()[:200]}")
        return False

    # Create GIF with palette
    cmd2 = [
        'ffmpeg', '-y', '-framerate', str(fps),
        '-i', frame_pattern,
        '-i', palette_path,
        '-lavfi', 'scale=720:-1:flags=lanczos,paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle',
        output_path
    ]
    result = subprocess.run(cmd2, capture_output=True)
    if result.returncode != 0:
        print(f"GIF creation failed: {result.stderr.decode()[:200]}")
        return False

    print(f"GIF created: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Capture Instagram Reel frames')
    parser.add_argument('url', help='Instagram reel URL')
    parser.add_argument('cookies_file', help='Netscape format cookies.txt file')
    parser.add_argument('output_dir', help='Output directory for frames and metadata')
    parser.add_argument('--percentages', default='0,14,28,42,57,71,86,99.9',
                       help='Comma-separated frame percentages')
    parser.add_argument('--fps', type=int, default=2, help='GIF framerate')
    parser.add_argument('--skip-gif', action='store_true', help='Skip GIF creation')
    args = parser.parse_args()

    percentages = [float(p.strip()) for p in args.percentages.split(',')]

    if not os.path.exists(args.cookies_file):
        print(f"ERROR: Cookies file not found: {args.cookies_file}")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Capture frames
    try:
        result = asyncio.run(capture_frames(args.url, args.cookies_file, args.output_dir, percentages))
    except Exception as e:
        print(f"ERROR: Frame capture failed: {e}")
        sys.exit(1)

    # Save metadata JSON
    meta_path = output_dir / 'capture_metadata.json'
    with open(meta_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Metadata saved: {meta_path}")

    # Create GIF
    if not args.skip_gif and result['frames']:
        gif_path = output_dir / f"{output_dir.name}.gif"
        create_gif(result['frames_dir'], str(gif_path), args.fps)

    # Print summary
    print(f"\n{'='*50}")
    print(f"CAPTURE COMPLETE")
    print(f"{'='*50}")
    print(f"URL: {result['url']}")
    print(f"Duration: {result['duration']}s")
    print(f"Resolution: {result['video_width']}x{result['video_height']}")
    print(f"Frames captured: {len(result['frames'])}")
    print(f"Frames dir: {result['frames_dir']}")
    print(f"Metadata: {meta_path}")
    if result.get('metadata'):
        print(f"Caption preview: {result['metadata'].get('caption', 'N/A')[:100]}...")
        print(f"Hashtags: {result['metadata'].get('hashtags', [])}")
    if not args.skip_gif:
        print(f"GIF: {output_dir / f'{output_dir.name}.gif'}")


if __name__ == '__main__':
    main()