from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"