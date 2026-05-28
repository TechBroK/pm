import os, requests, json
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENROUTER_API_KEY')
print('API key present:', bool(key))
headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
endpoints = [
    'https://openrouter.io/api/v1/chat/completions',
    'https://openrouter.ai/api/v1/chat/completions',
    'https://api.openrouter.ai/v1/chat/completions'
]
models = ['openai/gpt-3.5-turbo','openai/gpt-oss-120b','gpt-3.5-turbo','gpt-4o']
payload = {
    'model': models[0],
    'messages': [{'role':'user','content':'What is 2+2?'}],
    'temperature':0.7,
    'max_tokens':50
}
for e in endpoints:
    for m in models:
        payload['model']=m
        try:
            r = requests.post(e, headers=headers, json=payload, timeout=15)
            print('\nEndpoint:', e)
            print('Model:', m)
            print('Status:', r.status_code)
            text = r.text.strip()
            print('Text length:', len(text))
            if text:
                try:
                    print('JSON:', json.dumps(r.json(), indent=2)[:500])
                except Exception as ex:
                    print('Non-JSON response or parse error:', ex)
        except Exception as ex:
            print('\nEndpoint:', e)
            print('Model:', m)
            print('Error:', ex)
print('\nDone')
