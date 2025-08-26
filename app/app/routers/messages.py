from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.data_checks.messages import main as messages
from app.dependencies import get_db

message_router = APIRouter(prefix='/messages')

@message_router.post("/send-message/")
async def send_message(args: messages.IngoingMessage, db: Session = Depends(get_db)) -> str:
    return "Hello there"