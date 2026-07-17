import os
from groq import Groq
from dotenv import load_dotenv

# Load the secret keys and variables from the .env file
load_dotenv()

# Initialize the AI Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Pull the model names from .env, with hardcoded fallbacks just in case the .env is missing
PRIMARY_MODEL = os.environ.get("PRIMARY_LLM", "llama-3.1-8b-instant")
BACKUP_MODEL = os.environ.get("BACKUP_LLM", "mixtral-8x7b-32768")

def generate_linkedin_post(topic: str) -> str:
    """
    Takes a short user prompt and returns a fully formatted LinkedIn post,
    utilizing a fallback cascade for high availability.
    """
    
    system_prompt = """
    You are a highly successful tech-industry LinkedIn ghostwriter. 
    The user will give you a brief topic or scenario. 
    You must write a highly engaging, 3-paragraph LinkedIn post about it. 
    
    Rules:
    - Use a strong, attention-grabbing opening hook.
    - Keep the tone professional but authentic and slightly conversational.
    - Use line breaks for readability.
    - Include 2-3 relevant emojis.
    - End with 3-5 trending professional hashtags.
    - NEVER use cringe corporate jargon like 'synergy'.
    """
    
    try:
        # ATTEMPT 1: Fire the Primary Model
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a LinkedIn post about: {topic}"}
            ],
            model=PRIMARY_MODEL,
            temperature=0.7,
        )
        return response.choices[0].message.content
        
    except Exception as primary_error:
        print(f"⚠️ Primary model ({PRIMARY_MODEL}) failed. Engaging backup... Error: {primary_error}")
        
        try:
            # ATTEMPT 2: Fire the Backup Model
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Write a LinkedIn post about: {topic}"}
                ],
                model=BACKUP_MODEL,
                temperature=0.7,
            )
            return response.choices[0].message.content
            
        except Exception as backup_error:
            # ATTEMPT 3: Complete Failure
            return f"❌ Both models failed. Critical Error: {str(backup_error)}"

# Quick local test
if __name__ == "__main__":
    test_topic = "Why redundant fallback systems save engineering jobs."
    print("Generating post...\n")
    print(generate_linkedin_post(test_topic))