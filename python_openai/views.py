from django.shortcuts import render
from django.http import HttpResponse
import requests
import os

def index(request):
    user_input = ''
    if request.method == 'POST':
        user_input = request.POST['user_input']
        api_endpoint = "https://api.openai.com/v1/completions"
        api_key = os.environ.get('OPENAI_API_KEY')

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }

        request_data = {
            "model": "text-davinci-003",
            "prompt": f"Write python script to {user_input}. Provide only code, no text",
            "max_tokens": 500,
            "temperature": 0.5
        }

        response = requests.post(api_endpoint, headers=request_headers, json=request_data)

        if response.status_code == 200:
            response_text = response.json()["choices"][0]["text"]
            response = HttpResponse(response_text, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="my_script.py"'
            return response
        else:
            response = f"Request failed with status code: {str(response.status_code)}. Please try again"
            return render(request, 'python_openai/index.html', {'response': response})
            
    else:
        return render(request, 'python_openai/index.html', {'user_input': user_input})
    
