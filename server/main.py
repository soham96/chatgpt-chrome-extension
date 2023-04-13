import requests
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import os
import tone

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

#app.include_router(document_search.router)
app.include_router(tone.router)

@app.post("/router")
def router(data: dict = Body()):
    if data['action']=='summarize':
        return summarize(data)
    elif data['action']=='formalize':
        return formalize(data)
    elif data['action']=='translate':
        return translate(data)

@app.post("/translate")
def translate(data: dict = Body()):
    print(data)
    url = f"https://api.openai.com/v1/completions"

    prompt=f"Can you translate the following text to English. Return only the translated text and nothing else: \n '{data['text']}'"
    headers = {"Content-Type": "application/json",
                 "Authorization": f"Bearer {OPENAI_API_KEY}"}

    data={
          "model": "text-davinci-003",
          "prompt": prompt,
          "max_tokens": 1000,
          "temperature": 0.2,
          "top_p": 1,
          "n": 1,
  }
          
    # Send the POST request to the API endpoint
    print("Prompting")
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return {"output": response.json()['choices'][0]['text']} 

@app.post("/summarize")
def summarize(data: dict = Body()):
    print(data)
    url = f"https://api.openai.com/v1/completions"

    prompt=f"Can you summarize the following text. Return only the summarized text and nothing else: \n '{data['text']}'"
    headers = {"Content-Type": "application/json",
                 "Authorization": f"Bearer {OPENAI_API_KEY}"}

    data={
          "model": "text-davinci-003",
          "prompt": prompt,
          "max_tokens": 1000,
          "temperature": 0.2,
          "top_p": 1,
          "n": 1,
  }
          
    # Send the POST request to the API endpoint
    print("Prompting")
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    #import ipdb; ipdb.set_trace()
    return {"output": response.json()['choices'][0]['text']} 

@app.post("/formalize")
def formalize(data: dict = Body()):
    url = f"https://api.openai.com/v1/completions"

    prompt=f"Can you make the following text sound formal. Return only the expanded text and nothing else: \n '{data['text']}'"
    headers = {"Content-Type": "application/json",
                 "Authorization": f"Bearer {OPENAI_API_KEY}"}

    data={
          "model": "text-davinci-003",
          "prompt": prompt,
          "max_tokens": 1000,
          "temperature": 0.2,
          "top_p": 1,
          "n": 1,
  }
          
    # Send the POST request to the API endpoint
    print("Prompting")
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    #import ipdb; ipdb.set_trace()
    return {"output": response.json()['choices'][0]['text']} 

