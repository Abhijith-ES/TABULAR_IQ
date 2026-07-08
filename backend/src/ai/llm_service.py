from dotenv import load_dotenv
import os
from groq import Groq
import json


load_dotenv()

API_KEY=os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API Key is not configured.")

LLM_MODEL=os.getenv("LLM_MODEL")
if not LLM_MODEL:
    raise ValueError("LLM model not configured.")

client = Groq(api_key=API_KEY)

def _strip_response_wrappers(text: str) -> str:
    cleaned_text = text.strip()

    if "</think>" in cleaned_text:
        cleaned_text = cleaned_text.split("</think>", 1)[-1].strip()

    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text.replace("```json", "", 1).strip()

    if cleaned_text.startswith("```python"):
        cleaned_text = cleaned_text.replace("```python", "", 1).strip()

    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.replace("```", "", 1).strip()

    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3].strip()

    return cleaned_text

def _parse_llm_json(response: str) -> dict:
    cleaned_response = _strip_response_wrappers(response)

    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        json_start = cleaned_response.find("{")

        while json_start != -1:
            try:
                data, _ = decoder.raw_decode(cleaned_response[json_start:])
                return data
            except json.JSONDecodeError:
                json_start = cleaned_response.find("{", json_start + 1)

    raise ValueError("LLM response did not contain valid JSON.")

def generate_code(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": """
You are a code generation engine.
If the user query can be answered from dataset metadata, set result directly.
The code value will be directly passed into exec().
Any non-code text inside the code value will break the system.

Return ONLY a valid JSON object.
                 
Schema:
{
    "code": "<python pandas code>"
}

Never explain.
Never use markdown.
Never describe your reasoning.
Never include comments.
Your response must start directly with valid JSON.
"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
        response = response.choices[0].message.content
        print(response)
        data = _parse_llm_json(response)
        generated_code = _strip_response_wrappers(data["code"])
        
        if not generated_code.strip():
            raise ValueError("LLM doesn't provide any response.")
        
        try:
            compile(generated_code, "<generated>", "exec")

        except SyntaxError:
            raise ValueError(
                "LLM generated invalid Python code"
            )
        
        return generated_code.strip()
    
    except Exception:
        raise 