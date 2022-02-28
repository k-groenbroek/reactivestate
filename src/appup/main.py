from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
import uvicorn

from appup.core.page import page
from appup.core.mdx import compile


mdxdir = "src/appup/ui/"


def handle_mdx(request: Request):
    mdxpath = mdxdir + request.path_params["mdxfile"]
    content = compile(mdxpath)
    response = Response(content, media_type="text/javascript")
    return response


def app():
    app = Starlette()
    app.add_route("/mdx/{mdxfile:path}", handle_mdx)
    page(app, "/", "app.mdx")
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        factory=True,
        reload=True,
        reload_dirs=["src/appup"],
    )
