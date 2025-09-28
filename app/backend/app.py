from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
async def connection_test():
    return {"status": "SUCCESS"}