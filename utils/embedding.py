import numpy as np
from openai import OpenAI
from db import Session
from env import env

client = OpenAI(api_key=env.OPENAI_API_KEY)

def generate_embedding(text: str) -> list[float]:
    if not text.strip():
        return np.zeros(1536).tolist()
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
