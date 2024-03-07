from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataIn(BaseModel):
    data: str


class DataOut(BaseModel):
    data: str

class Message(BaseModel):
    message: str

@app.post("/chat")
async def process_message(message: Message):
    answer = message.message + ", zdarova "

    return {"response": f"{answer}"}
