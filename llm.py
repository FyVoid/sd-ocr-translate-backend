import requests
from config import CONFIG

# TODO: add error logging

def remove_tag(text: str, tag: str) -> str:
    tag_start = f'<{tag}>'
    tag_end = f'</{tag}>'
    if tag_start in text and tag_end in text:
        text = text.replace(tag_start, '').replace(tag_end, '')

    return text

def to_llm(text: str, sys_prompt: str = CONFIG['llm']['system_prompt'], remove_thinking: bool = True) -> str:
    url = CONFIG['llm']['url']
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CONFIG['llm']['api-key']}",
    }
    payload = {
        "model": CONFIG['llm']['model'],
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": text},
        ],
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    text = response.json()["choices"][0]["message"]["content"]
    
    if remove_thinking:
        return remove_tag(text, 'think')

    return text