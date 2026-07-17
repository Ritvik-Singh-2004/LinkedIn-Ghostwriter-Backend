import os
from groq import Groq
from dotenv import load_dotenv

#Loading the API key from .env
load_dotenv()

client=Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_linkedin_post(topic:str)->str:
    """
    Takes a short user input and returns a fully formatted LinkedIn post.
    """
    
    # Prompt Engineer
    
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
    - NEVER use cringe corporate jargon like 'synergy' or 'think outside the box'.
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {"role":"system" , "content" : system_prompt},
                {"role":"user" , "content" : f"Write a LinkedIn post about {topic}"}
            ],
            model="llama-3.1-8b-instant", # The upgraded, active Llama 3.1 model
            temperature=0.7 #good mix of creativity and structure, apparently
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating post: {str(e)}"

# A local test to ensure working
if __name__ == "__main__":
    test_topic="I finlly learned how to use the Groq API for LinkedIn post generation!"
    print("Generating post...\n")

    print(generate_linkedin_post(test_topic))