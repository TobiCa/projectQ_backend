from fastapi import FastAPI
from app.routers.messages import message_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router, tags=["message"])

@app.get("/")
async def root():
    return {"message": "hello"}
