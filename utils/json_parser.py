import json
import re

def json_output_parser(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Raw LLM output:", text)
        json_match = re.search(r'(\{.*\})', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError as inner_e:
                print("Failed to parse extracted JSON:", inner_e)
                raise inner_e
        else:
            raise e
