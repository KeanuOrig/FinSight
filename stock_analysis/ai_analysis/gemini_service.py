from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai
import os

# Create your views here.
# add here to your generated API key
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-002")
        chat = model.start_chat()
        response = chat.send_message(prompt)
        print(response.text)

        
        return response.text
    except Exception as e:
        print(f"Error while interacting with Gemini API: {e}")
        return f"Error interacting with Gemini API: {str(e)}"