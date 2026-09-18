import json

with open('/Users/alfredkamisese/.hermes/skills/communication/tongan-translation/cache/translate-pack.json') as f:
    pack = json.load(f)

pos = pack['data']['possessive']['index']
targets = ["eiki", "tu'i", "otua", "lea", "lotu", "siasi", "fale", "taimi", "hala", "mafai", "tu'ung"]

found = []
for entry in pos:
    noun = str(entry.get('noun', '')).lower()
    for t in targets:
        if t in noun:
            found.append((entry.get('noun'), entry.get('class'), entry.get('notes', '')))
            break

for f in found:
    print(' ', f)

print('\nTotal possessive nouns:', len(pos))

# Also check few-shot verified examples for lord/shepherd/god usage
examples = pack['data'].get('few_shot', {}).get('tagged', [])
for ex in examples:
    to = ex.get('tongan', '')
    if any(k in to for k in ["'Otua", "'Eiki", "tu'i", "Siasi", "lotu"]):
        print('EXAMPLE:', ex.get('english'), '=>', to, '|', ex.get('frame'))