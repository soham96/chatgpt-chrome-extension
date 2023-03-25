import requests
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import os

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

app = FastAPI()

print('here')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )


@app.post("/expand")
def expand(data: dict = Body()):
    url = f"https://api.openai.com/v1/completions"

    prompt=f"Can you expand the following text: \n '{data['message']}'"
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
    return {"reply": response.json()['choices'][0]['text']} 

