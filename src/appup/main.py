from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import uvicorn

from appup.core.page import page


def app():
    app = Starlette()
    app.mount("/components", StaticFiles(directory="src/appup/components"))

    with page(app, "/") as p:
        p.markdown("# My App")
        mylist = p.ul()
        for i in range(10):
            mylist.li().text(f"Item {i}")
        p.button().text("click me")

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
