#!/usr/bin/env python3
"""
CFM Cron Command — Orchestrates the Come Follow Me study guide generation pipeline.

Pipeline:
1. Run Helios' CFM skill to fetch/generate doctrinal content (JSON)
2. Call Apollo's render_cfm_mobile(data, 'eq') to get themed HTML
3. Write HTML to both output folders (Teacher + Personal)
4. Use Chrome headless to generate PDF from HTML
5. Output: HTML + PDF in both folders

Usage:
    python3 cron_command.py --week "2026-04-week-14" --output-base "~/Desktop/Elders Quorum Lessons 2025.2026/2026/04"
    python3 cron_command.py --auto  # Auto-detect current week

Environment:
    CFM_SKILL_PATH: Path to come-follow-me-study-guide skill (default: ~/.hermes/profiles/helios/skills/religious-study/come-follow-me-study-guide)
    APOLLO_RENDERER_PATH: Path to Apollo's render_cfm_mobile module
"""

import json
import argparse
import sys
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import importlib.util

# ========================================
# CONFIGURATION
# ========================================
DEFAULT_SKILL_PATH = Path.home() / ".hermes" / "profiles" / "helios" / "skills" / "religious-study" / "come-follow-me-study-guide"
DEFAULT_OUTPUT_BASE = Path.home() / "Desktop" / "Elders Quorum Lessons 2025.2026"

# EQ Color tokens (from Apollo)
EQ_COLORS = {
    "scripture": "#0d5d3a",      # emerald - priesthood
    "gold": "#b8963e",           # brass - EQ branding
    "dark_brass": "#8b7330",
    "warm_white": "#fdfbf7",
    "light_gold": "#f5ebe0"
}

# ========================================
# UTILITY FUNCTIONS
# ========================================
def log(msg: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {msg}")

def run_command(cmd: list, cwd: Path = None, capture: bool = True) -> Tuple[int, str, str]:
    """Run a shell command, return (exit_code, stdout, stderr)."""
    log(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True, timeout=300)
        if result.stdout and capture:
            log(result.stdout.strip(), "DEBUG")
        if result.stderr and capture:
            log(result.stderr.strip(), "WARN")
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def find_chrome() -> Optional[str]:
    """Find Chrome/Chromium executable for headless PDF generation."""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    # Try which
    for name in ["google-chrome", "chromium", "chromium-browser"]:
        code, out, _ = run_command(["which", name])
        if code == 0 and out.strip():
            return out.strip()
    return None

# ========================================
# STEP 1: RUN CFM SKILL (Helios)
# ========================================
def run_cfm_skill(skill_path: Path, week_id: str) -> Dict[str, Any]:
    """
    Run Helios' come-follow-me-study-guide skill to get doctrinal content.
    Expected to output JSON to stdout or write to a known location.
    """
    log(f"Running CFM skill for week: {week_id}")
    
    # The skill should be invokable via Hermes or directly
    # For now, we'll look for a generate_lesson.py or similar in the skill
    skill_script = skill_path / "scripts" / "generate_lesson.py"
    if not skill_script.exists():
        # Try alternative locations
        skill_script = skill_path / "generate_lesson.py"
    if not skill_script.exists():
        skill_script = skill_path / "scripts" / "fetch_lesson.py"
    
    if skill_script.exists():
        code, stdout, stderr = run_command([sys.executable, str(skill_script), "--week", week_id], cwd=skill_path)
        if code == 0:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                # Maybe it writes to a file
                pass
    
    # Fallback: check for pre-generated data file
    data_file = skill_path / "data" / f"{week_id}.json"
    if data_file.exists():
        with open(data_file) as f:
            return json.load(f)
    
    # Fallback: generate from manual template (for testing)
    log("No skill output found, using template data", "WARN")
    template_file = skill_path / "sample-lesson-data.json"
    if template_file.exists():
        with open(template_file) as f:
            data = json.load(f)
            data["lessonId"] = week_id
            return data
    
    raise RuntimeError(f"Could not generate lesson data for {week_id}")

# ========================================
# STEP 2: CALL APOLLO'S RENDERER
# ========================================
def load_apollo_renderer(renderer_path: str = None):
    """Load Apollo's render_cfm_mobile function."""
    if renderer_path:
        spec = importlib.util.spec_from_file_location("apollo_renderer", renderer_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.render_cfm_mobile
    
    # Try common locations
    search_paths = [
        Path.home() / ".hermes" / "profiles" / "apollo" / "skills" / "render_cfm_mobile.py",
        Path.home() / ".hermes" / "profiles" / "apollo" / "render_cfm_mobile.py",
        Path("/Users/alfredkamisese") / "apollo_render_cfm_mobile.py",
    ]
    
    for p in search_paths:
        if p.exists():
            spec = importlib.util.spec_from_file_location("apollo_renderer", p)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            log(f"Loaded Apollo renderer from {p}")
            return module.render_cfm_mobile
    
    # Try import if installed as package
    try:
        from apollo import render_cfm_mobile
        return render_cfm_mobile
    except ImportError:
        pass
    
    log("Apollo renderer not found - will use fallback template", "WARN")
    return None

def render_with_apollo(data: Dict[str, Any], mode: str = "eq") -> str:
    """Call Apollo's renderer or fallback to local template."""
    renderer = load_apollo_renderer()
    
    if renderer:
        log("Calling Apollo's render_cfm_mobile()")
        try:
            html = renderer(data, mode)
            if not html or not isinstance(html, str):
                raise ValueError("Renderer returned invalid HTML")
            return html
        except Exception as e:
            log(f"Apollo renderer failed: {e}, using fallback", "ERROR")
    
    # Fallback: use our local template with CFMTemplate.setLessonData injection
    return render_with_fallback_template(data)

def render_with_fallback_template(data: Dict[str, Any]) -> str:
    """Fallback: inject data into our enhanced template."""
    template_path = DEFAULT_SKILL_PATH / "templates" / "study-guide-template.html"
    with open(template_path) as f:
        template = f.read()
    
    # Inject initialization script with data
    init_script = f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            if (window.CFMTemplate) {{
                window.CFMTemplate.setLessonData({json.dumps(data, ensure_ascii=False)});
            }}
        }});
    </script>
    """
    html = template.replace('</body>', init_script + '\n</body>')
    
    # Apply EQ color overrides via inline style
    eq_style = f"""
    <style>
        :root {{
            --accent-primary: {EQ_COLORS['gold']};
            --accent-secondary: {EQ_COLORS['dark_brass']};
            --accent-light: {EQ_COLORS['light_gold']};
            --text-primary: {EQ_COLORS['scripture']};
            --bg-primary: {EQ_COLORS['warm_white']};
            --bg-tertiary: {EQ_COLORS['light_gold']};
        }}
        [data-theme="dark"] {{
            --accent-primary: {EQ_COLORS['gold']};
            --accent-secondary: {EQ_COLORS['dark_brass']};
            --text-primary: {EQ_COLORS['warm_white']};
            --bg-primary: #0f1a22;
            --bg-tertiary: #1a2a36;
        }}
    </style>
    """
    html = html.replace('</head>', eq_style + '\n</head>')
    
    return html

# ========================================
# STEP 3: WRITE HTML FILES
# ========================================
def write_html_files(html: str, week_id: str, output_base: Path, personal: bool = False) -> Tuple[Path, Path]:
    """Write HTML to Teacher and/or Personal folders."""
    teacher_dir = output_base / "Teacher Lessons"
    personal_dir = output_base / "Personal Study"
    
    teacher_dir.mkdir(parents=True, exist_ok=True)
    personal_dir.mkdir(parents=True, exist_ok=True)
    
    suffix = "-personal" if personal else "-teacher"
    filename = f"{week_id}{suffix}.html"
    
    teacher_path = teacher_dir / filename
    personal_path = personal_dir / filename
    
    # Write teacher version (always)
    with open(teacher_path, 'w', encoding='utf-8') as f:
        f.write(html)
    log(f"Written: {teacher_path}")
    
    # Write personal version (if requested or always for both)
    if personal:
        # Personal version could have different data (e.g., no teaching prompts)
        personal_html = html.replace('-teacher', '-personal')
        with open(personal_path, 'w', encoding='utf-8') as f:
            f.write(personal_html)
        log(f"Written: {personal_path}")
    
    return teacher_path, personal_path

# ========================================
# STEP 4: GENERATE PDF (Chrome Headless)
# ========================================
def generate_pdf(html_path: Path, pdf_path: Path, chrome_path: str = None) -> bool:
    """Generate PDF from HTML using Chrome headless."""
    if not chrome_path:
        chrome_path = find_chrome()
    
    if not chrome_path:
        log("Chrome/Chromium not found - skipping PDF generation", "WARN")
        return False
    
    log(f"Generating PDF: {pdf_path}")
    
    # Chrome headless print-to-PDF options
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--print-to-pdf=" + str(pdf_path),
        "--print-to-pdf-no-header",
        "--virtual-time-budget=10000",
        str(html_path)
    ]
    
    code, stdout, stderr = run_command(cmd, capture=False)
    
    if code == 0 and pdf_path.exists():
        log(f"PDF generated: {pdf_path} ({pdf_path.stat().st_size} bytes)")
        return True
    else:
        log(f"PDF generation failed: {stderr}", "ERROR")
        return False

# ========================================
# STEP 5: AUTO-DETECT CURRENT WEEK
# ========================================
def get_current_week_id() -> str:
    """Calculate current CFM week ID (YYYY-MM-week-N)."""
    # CFM year starts first week of January
    today = datetime.now()
    year = today.year
    
    # Find first Monday of January
    jan1 = datetime(year, 1, 1)
    days_until_monday = (7 - jan1.weekday()) % 7  # Monday = 0
    first_monday = jan1 + timedelta(days=days_until_monday)
    
    if today < first_monday:
        year -= 1
        jan1 = datetime(year, 1, 1)
        days_until_monday = (7 - jan1.weekday()) % 7
        first_monday = jan1 + timedelta(days=days_until_monday)
    
    # Calculate week number (1-indexed)
    days_diff = (today - first_monday).days
    week_num = (days_diff // 7) + 1
    
    # Clamp to 1-52
    week_num = max(1, min(52, week_num))
    
    return f"{year}-{week_num:02d}"

# ========================================
# MAIN ORCHESTRATION
# ========================================
def main():
    parser = argparse.ArgumentParser(description="CFM Cron Command - Generate study guides")
    parser.add_argument("--week", help="Week ID (e.g., 2026-14)")
    parser.add_argument("--auto", action="store_true", help="Auto-detect current week")
    parser.add_argument("--output-base", default=str(DEFAULT_OUTPUT_BASE), help="Base output directory")
    parser.add_argument("--skill-path", default=str(DEFAULT_SKILL_PATH), help="Path to CFM skill")
    parser.add_argument("--apollo-renderer", help="Path to Apollo's render_cfm_mobile.py")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    parser.add_argument("--personal", action="store_true", help="Also generate personal study version")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files, just log")
    
    args = parser.parse_args()
    
    # Determine week
    if args.auto:
        week_id = get_current_week_id()
        log(f"Auto-detected week: {week_id}")
    elif args.week:
        week_id = args.week
    else:
        parser.error("Either --week or --auto required")
    
    output_base = Path(args.output_base).expanduser()
    skill_path = Path(args.skill_path).expanduser()
    
    log(f"=== CFM Cron Job Started ===")
    log(f"Week: {week_id}")
    log(f"Output base: {output_base}")
    log(f"Skill path: {skill_path}")
    log(f"Personal version: {args.personal}")
    log(f"PDF generation: {not args.no_pdf}")
    
    try:
        # Step 1: Get doctrinal content from CFM skill
        data = run_cfm_skill(skill_path, week_id)
        data["lessonId"] = week_id
        data["generationDate"] = datetime.now().strftime("%B %d, %Y")
        
        # Step 2: Render HTML via Apollo (or fallback)
        html = render_with_apollo(data, mode="eq")
        
        if args.dry_run:
            log("DRY RUN - HTML preview (first 500 chars):")
            log(html[:500])
            return 0
        
        # Step 3: Write HTML files
        teacher_html, personal_html = write_html_files(html, week_id, output_base, args.personal)
        
        # Step 4: Generate PDFs
        if not args.no_pdf:
            chrome = find_chrome()
            if chrome:
                teacher_pdf = teacher_html.with_suffix(".pdf")
                generate_pdf(teacher_html, teacher_pdf, chrome)
                
                if args.personal:
                    personal_pdf = personal_html.with_suffix(".pdf")
                    generate_pdf(personal_html, personal_pdf, chrome)
            else:
                log("Chrome not found - PDF generation skipped", "WARN")
        
        log("=== CFM Cron Job Completed Successfully ===")
        return 0
        
    except Exception as e:
        log(f"FATAL ERROR: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())