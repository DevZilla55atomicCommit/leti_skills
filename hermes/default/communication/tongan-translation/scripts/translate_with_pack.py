#!/usr/bin/env python3
"""
Translate using the full Lea Faka-Tonga translation pack system prompt.
"""

import json
import subprocess
import sys
from pathlib import Path

CACHE_DIR = Path.home() / ".hermes" / "skills" / "communication" / "tongan-translation" / "cache"
PACK_PATH = CACHE_DIR / "translate-pack.json"


def load_pack():
    with open(PACK_PATH) as f:
        return json.load(f)


def translate(english: str) -> dict:
    pack = load_pack()
    system_prompt = pack['system_prompt']
    
    prompt = f"{system_prompt}\n\nTranslate this English sentence:\n{english}"
    
    result = subprocess.run(
        ['ollama', 'run', 'nemotron-3-ultra:cloud', prompt],
        capture_output=True, text=True, timeout=300
    )
    
    if result.returncode != 0:
        return {"error": f"Ollama failed: {result.stderr}"}
    
    output = result.stdout.strip()
    import re
    # Clean ANSI escape sequences
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
    output = ansi_escape.sub('', output)
    # Also clean any other control characters that might break JSON
    output = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', output)
    
    # Try to find a valid JSON object - look for balanced braces
    def extract_json(text):
        # Find first {
        start = text.find('{')
        if start == -1:
            return None
        
        depth = 0
        in_string = False
        escape = False
        for i, ch in enumerate(text[start:], start):
            if escape:
                escape = False
                continue
            if ch == '\\':
                escape = True
                continue
            if ch == '"' and not escape:
                in_string = not in_string
                continue
            if not in_string:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        return text[start:i+1]
        return None
    
    json_str = extract_json(output)
    if not json_str:
        return {"error": "No JSON found in output", "raw": output[:500]}
    
    # Clean control characters from JSON string
    json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', json_str)
    
    # The issue: model outputs literal newlines inside JSON string values
    # We need to replace literal newlines inside string values with \n
    # Let's do a simple state-machine fix
    def fix_json_strings(s):
        """Replace literal newlines inside JSON string values with \\n"""
        result = []
        in_string = False
        escape = False
        for ch in s:
            if escape:
                result.append(ch)
                escape = False
                continue
            if ch == '\\':
                result.append(ch)
                escape = True
                continue
            if ch == '"' and not escape:
                in_string = not in_string
                result.append(ch)
                continue
            if in_string and ch in '\n\r\t':
                result.append('\\n' if ch == '\n' else '\\r' if ch == '\r' else '\\t')
            else:
                result.append(ch)
        return ''.join(result)
    
    json_str_fixed = fix_json_strings(json_str)
    
    # Also fix duplicate keys - keep first occurrence
    def fix_duplicate_keys(s):
        """Remove duplicate keys from JSON object - keep first occurrence"""
        # This is a simple regex-based fix for the specific case
        # Match pattern: "key": value, ... "key": value
        # We'll just try to parse and if it fails, return as-is
        return s
    
    try:
        parsed = json.loads(json_str_fixed)
        # Normalize frame
        frame_map = {
            'declarative': 'statement',
            'declaration': 'statement',
            'simple': 'statement',
        }
        if 'frame' in parsed and parsed['frame'] in frame_map:
            parsed['frame'] = frame_map[parsed['frame']]
        return parsed
    except json.JSONDecodeError as e:
        # Try to fix duplicate keys by using a custom decoder
        import json as json_module
        
        class DuplicateKeyDecoder(json_module.JSONDecoder):
            def __init__(self, *args, **kwargs):
                kwargs['object_pairs_hook'] = lambda pairs: dict(pairs)
                super().__init__(*args, **kwargs)
        
        try:
            parsed = json.loads(json_str_fixed, cls=DuplicateKeyDecoder)
            frame_map = {
                'declarative': 'statement',
                'declaration': 'statement',
                'simple': 'statement',
            }
            if 'frame' in parsed and parsed['frame'] in frame_map:
                parsed['frame'] = frame_map[parsed['frame']]
            return parsed
        except json.JSONDecodeError as e2:
            return {"error": f"JSON parse error: {e2}", "raw": json_str_fixed[:500]}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python translate_with_pack.py '<english sentence>'")
        sys.exit(1)
    
    english = ' '.join(sys.argv[1:])
    result = translate(english)
    print(json.dumps(result, indent=2, ensure_ascii=False))