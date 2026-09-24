#!/usr/bin/env python3
"""
List installed Ollama models with size and modification date.
Useful before generating images to verify required model availability.
"""

import subprocess
import sys
from datetime import datetime

def parse_model_line(line):
    """Extract model name, size, and tags from ' ollama list' output line."""
    parts = line.strip().split()
    if len(parts) >= 3:
        return {
            'model': parts[0],
            'size': parts[1],
            'digest': parts[2],
        }
    return None

def main():
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print(f'Error running ollama list: {result.stderr}', file=sys.stderr)
            sys.exit(1)
            
        models = []
        lines = result.stdout.strip().split('\n')
        # Skip header line (first line)
        for line in lines[1:]:
            model_info = parse_model_line(line)
            if model_info:
                models.append(model_info)
                
        if not models:
            print('No models found.')
            return
            
        print('Installed Ollama models:')
        print('-' * 60)
        for model in models:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            print(f'{model["model"]:<20} {model["size"]:<10} {model["digest"][:12]}...  {timestamp}')
            
    except subprocess.TimeoutExpired:
        print('Timeout: ollama list took too long', file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print('Error: ollama command not found. Please install Ollama first.', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()