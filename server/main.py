from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.routing import Route, Mount
import uvicorn

from core.page import page, Tag


def app():
    app = Starlette()
    app.mount("/components", StaticFiles(directory="server/components"))
    with page(app, "/") as p:
        p += "# My app"
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        factory=True,
        reload=True,
        reload_dirs=["server"],
    )
