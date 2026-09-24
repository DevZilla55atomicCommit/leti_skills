#!/usr/bin/env python3
"""
Tongan Translation CLI — uses the Lea Faka-Tonga compiled translation pack.

Usage:
    python tongan_translate.py "I am going to the market"
    python tongan_translate.py "Thank you" --model ollama:nemotron-3-ultra
    python tongan_translate.py --validate "Ko e tōketā koe"
"""

import json
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Asset URLs (from joakimandrew-cloud/lea-faka-tonga)
PACK_URL = "https://raw.githubusercontent.com/joakimandrew-cloud/lea-faka-tonga/main/src/data/translate-pack.json"
ALLOWSET_URL = "https://raw.githubusercontent.com/joakimandrew-cloud/lea-faka-tonga/main/src/data/translate-allowset.json"
VOCAB_URL = "https://raw.githubusercontent.com/joakimandrew-cloud/lea-faka-tonga/main/src/data/book-vocabulary.json"

# Local cache directory
CACHE_DIR = Path.home() / ".hermes" / "skills" / "communication" / "tongan-translation" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

PACK_PATH = CACHE_DIR / "translate-pack.json"
ALLOWSET_PATH = CACHE_DIR / "translate-allowset.json"
VOCAB_PATH = CACHE_DIR / "book-vocabulary.json"


def download_if_missing(url: str, dest: Path, name: str) -> bool:
    """Download a file if it doesn't exist locally."""
    if dest.exists():
        return True
    try:
        import urllib.request
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, dest)
        print(f"  Saved to {dest}")
        return True
    except Exception as e:
        print(f"Failed to download {name}: {e}")
        return False


def load_pack() -> Optional[Dict]:
    """Load the translation pack."""
    if download_if_missing(PACK_URL, PACK_PATH, "translate-pack.json"):
        try:
            with open(PACK_PATH) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading pack: {e}")
    return None


def load_allowset() -> Optional[Dict]:
    """Load the allow-set for validation."""
    if download_if_missing(ALLOWSET_URL, ALLOWSET_PATH, "translate-allowset.json"):
        try:
            with open(ALLOWSET_PATH) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading allow-set: {e}")
    return None


def load_vocab() -> Optional[list]:
    """Load the vocabulary."""
    if download_if_missing(VOCAB_URL, VOCAB_PATH, "book-vocabulary.json"):
        try:
            with open(VOCAB_PATH) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading vocabulary: {e}")
    return None


def fold_tongan(word: str) -> str:
    """Fold a Tongan word per the allow-set rules."""
    FAKAUA = 'ʻ'
    import re
    word = str(word)
    word = word.replace("'", FAKAUA).replace(''', FAKAUA).replace(''', FAKAUA).replace('`', FAKAUA).replace('´', FAKAUA)
    import unicodedata
    word = unicodedata.normalize('NFD', word)
    word = ''.join(c for c in word if unicodedata.category(c) != 'Mn')
    word = word.lower()
    word = re.sub(f'^[^a-z{FAKAUA}]+', '', word)
    word = re.sub(f'[^a-z{FAKAUA}]+$', '', word)
    return word


def validate_tongan(sentence: str, allowset: Dict) -> Dict[str, Any]:
    """Validate a Tongan sentence against the allow-set."""
    tokens = sentence.replace('*', ' ').replace('_', ' ').replace('`', ' ').replace('~', ' ')
    tokens = tokens.replace('[', ' ').replace(']', ' ').replace('(', ' ').replace(')', ' ')
    tokens = tokens.split()
    
    allowed = set(allowset.get('tokens', []))
    CORE_BUCKETS = {'eald', 'book-vocabulary', 'grammar-graph', 'particles-and-paradigm'}
    
    results = []
    all_pass = True
    for tok in tokens:
        folded = fold_tongan(tok)
        if not folded:
            continue
        in_set = folded in allowed
        buckets = allowset.get('bucketsOf', {}).get(folded, set())
        core = any(b in CORE_BUCKETS for b in buckets)
        results.append({
            'original': tok,
            'folded': folded,
            'allowed': in_set,
            'core_bucket': core,
            'buckets': list(buckets)
        })
        if not in_set:
            all_pass = False
    
    return {'valid': all_pass, 'tokens': results}


def translate_with_llm(english: str, system_prompt: str, model: str = "nemotron-3-ultra:cloud") -> Optional[Dict]:
    """Call an LLM with the translation system prompt."""
    # Use ollama directly with the cloud model
    try:
        ollama_model = model.replace('ollama:', '')
        prompt = f"{system_prompt}\n\nTranslate this English sentence:\n{english}"
        result = subprocess.run(
            ['ollama', 'run', ollama_model, prompt],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            import re
            # Extract JSON from the output (model may include thinking text)
            match = re.search(r'\{.*\}', output, re.DOTALL)
            if match:
                parsed = json.loads(match.group())
                # Normalize frame name - map common variations to valid frames
                frame_map = {
                    'declarative': 'statement',
                    'declaration': 'statement',
                    'simple': 'statement',
                }
                if 'frame' in parsed and parsed['frame'] in frame_map:
                    parsed['frame'] = frame_map[parsed['frame']]
                return parsed
        else:
            print(f"Ollama stderr: {result.stderr}")
    except Exception as e:
        print(f"Ollama error: {e}")
    
    return None


def translate_tongan_to_english(tongan: str) -> Optional[str]:
    """Use the repo's translate.js engine via Node."""
    # This would need the full repo cloned; for now return None
    # TODO: implement when repo is cloned locally
    return None


def main():
    parser = argparse.ArgumentParser(description="Tongan Translation CLI (Lea Faka-Tonga)")
    parser.add_argument('text', nargs='*', help='Text to translate (English→Tongan) or validate (Tongan)')
    parser.add_argument('--model', default='ollama:nemotron-3-ultra', help='LLM model to use')
    parser.add_argument('--validate', action='store_true', help='Validate Tongan sentence against allow-set')
    parser.add_argument('--vocab', action='store_true', help='Look up Tongan word in vocabulary')
    parser.add_argument('--reverse', action='store_true', help='Translate Tongan→English (requires local repo)')
    parser.add_argument('--update', action='store_true', help='Force re-download assets')
    parser.add_argument('--show-prompt', action='store_true', help='Print the system prompt and exit')
    
    args = parser.parse_args()
    
    # Force update
    if args.update:
        for p in [PACK_PATH, ALLOWSET_PATH, VOCAB_PATH]:
            if p.exists():
                p.unlink()
    
    # Load assets
    pack = load_pack()
    if not pack:
        print("Failed to load translation pack", file=sys.stderr)
        return 1
    
    system_prompt = pack.get('system_prompt', '')
    
    if args.show_prompt:
        print(system_prompt)
        return 0
    
    if args.validate:
        allowset = load_allowset()
        if not allowset:
            print("Failed to load allow-set", file=sys.stderr)
            return 1
        text = ' '.join(args.text)
        if not text:
            print("Usage: tongan_translate.py --validate '<tongan sentence>'")
            return 1
        result = validate_tongan(text, allowset)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result['valid'] else 1
    
    if args.vocab:
        vocab = load_vocab()
        if not vocab:
            print("Failed to load vocabulary", file=sys.stderr)
            return 1
        query = ' '.join(args.text).lower()
        if not query:
            print("Usage: tongan_translate.py --vocab <tongan word>")
            return 1
        matches = [v for v in vocab if query in v.get('tongan', '').lower() or query in v.get('english', '').lower()]
        for m in matches[:20]:
            print(f"  {m['tongan']} — {m['english']} ({m.get('part_of_speech', '')})")
        if not matches:
            print("No matches found")
        return 0
    
    if args.reverse:
        text = ' '.join(args.text)
        if not text:
            print("Usage: tongan_translate.py --reverse '<tongan sentence>'")
            return 1
        result = translate_tongan_to_english(text)
        if result:
            print(result)
        else:
            print("Reverse translation requires local repo clone (not implemented yet)")
        return 0
    
    # Default: English → Tongan
    english = ' '.join(args.text)
    if not english:
        print("Usage: tongan_translate.py '<english sentence>'")
        print("       tongan_translate.py --validate '<tongan sentence>'")
        print("       tongan_translate.py --vocab <tongan word>")
        return 1
    
    print(f"Translating: {english}")
    result = translate_with_llm(english, system_prompt, args.model)
    
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Validate output if it's a translation
        if 'tongan' in result:
            allowset = load_allowset()
            if allowset:
                validation = validate_tongan(result['tongan'], allowset)
                if not validation['valid']:
                    print("\n⚠ Validation warnings:")
                    for tok in validation['tokens']:
                        if not tok['allowed']:
                            print(f"  Token '{tok['original']}' (folded: {tok['folded']}) not in allow-set!")
    else:
        print("Translation failed", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())