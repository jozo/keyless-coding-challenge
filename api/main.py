from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.config import HOST, PORT

app = FastAPI()


@app.get("/api/", response_class=ORJSONResponse)
async def api_all():
    return {"hello": "world"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
