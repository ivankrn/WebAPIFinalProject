from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import models
import uvicorn

from database import engine
from routes import router_websocket, router_categories, router_bugs

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="BugTrackerWebApi",
    summary="Баг - трекер",
    version="1.0",
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    if http_protocol == "https":
        ws_protocol = "wss"
    else:
        ws_protocol = "ws"
    server_url = request.url.netloc
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "server_urn": server_url,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol}
                                       )


app.include_router(router_websocket)
app.include_router(router_bugs)
app.include_router(router_categories)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)