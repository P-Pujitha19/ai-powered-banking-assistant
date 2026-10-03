import json
import re

def mask_sensitive_data(data):
    """Mask account numbers and customer identifiers before response generation."""
    text = json.dumps(data, ensure_ascii=False)
    text = re.sub(r'(\d{4,})(?=")', lambda m: "X" * max(0, len(m.group(1))-4) + m.group(1)[-4:], text)
    text = re.sub(r'"account_number":\s*"[^"]+"', '"account_number": "XXXX1234"', text)
    return json.loads(text)
