from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated
import os
from dotenv import load_dotenv

from openai import OpenAI

app = FastAPI()

#The API key should never live within your code. Create a .env and use the os and python-doenv packages to read it
client = OpenAI(api_key='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')

@app.get("/")
def warmup():
    return {"message": "we're deployed and live!"}



#Defining the schema for our input data and setting some base default values
class jokeContext(BaseModel):
    topic: Annotated[str, Field(min_length=3, max_length=20)] = "random topic"
    age: Annotated[int, Field(ge=1, le=100)] = 10

#the api route that will take in our input and return a chatGPT generated joke
@app.post("/jokeGPT/")
async def create_joke(jokeContext: jokeContext):
    
#The call below uses f strings which come in very handy when doing any type of prompt engineering work for LLMs
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a joke writer"},
            {"role": "user", "content": f"Write me a joke about a {jokeContext.topic} for a {jokeContext.age} year old"}
        ],
    )
    return completion.choices[0].message.content.replace("\n", " ")