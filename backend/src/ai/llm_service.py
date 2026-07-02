from dotenv import load_dotenv
import os
from groq import Groq


load_dotenv()

API_KEY=os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API Key is not configured.")

LLM_MODEL=os.getenv("LLM_MODEL")
if not LLM_MODEL:
    raise ValueError("LLM model not configured.")

client = Groq(api_key=API_KEY)

def generate_code(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        generated_code = response.choices[0].message.content

        if generated_code.startswith("```python"):
            generated_code = generated_code.replace("```python","",1)

        if generated_code.startswith("```"):
            generated_code = generated_code.replace("```","",1)
            
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
        
        if not generated_code.strip():
            raise ValueError("LLM doesn't provide any response.")
        
        return generated_code.strip()
    
    except Exception:
        raise 

    
    


