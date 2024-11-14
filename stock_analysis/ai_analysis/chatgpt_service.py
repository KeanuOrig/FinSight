from openai import OpenAI
import os

""" Not used, no free tier """
def get_chatgpt_response(prompt):
    try:
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "test"}
            ]
        )
        
        response = OpenAI.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error while interacting with OpenAI API: {e}")
        return f"Error interacting with OpenAI API: {str(e)}"