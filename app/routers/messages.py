from fastapi import APIRouter, Depends
from app.data_checks.messages import main as messages

message_router = APIRouter(prefix='/messages')

@message_router.post("/send-message/")
async def send_message(args: messages.IngoingMessage) -> str:
    return "Hello there"