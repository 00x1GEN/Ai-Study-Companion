import json

def parse_json_array(raw: str) -> list:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    start, end = text.find("["), text.rfind("]")
    if start < 0 or end < start:
        raise ValueError("No JSON array found")
    data = json.loads(text[start:end + 1])
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array")
    return data
