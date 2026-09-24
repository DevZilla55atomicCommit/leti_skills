import subprocess
import sys
sys.path.insert(0, '/Users/alfredkamisese/.hermes/skills/communication/tongan-translation/scripts')
from translate_with_pack import translate
import time

tests = [
    "The Lord is my God.",
    "God is in the house.",
    "I trust in God.",
    "The king is in the church.",
]

for t in tests:
    print('===', t)
    result = translate(t)
    if 'error' in result:
        print('  ERROR:', result['error'][:100])
    elif result.get('escalate'):
        print('  ESCALATED:', result.get('escalate_reason', '')[:120])
    else:
        print('  TONGAN:', result.get('tongan', ''))
        print('  frame:', result.get('frame'), 'conf:', result.get('confidence'))
    time.sleep(2)