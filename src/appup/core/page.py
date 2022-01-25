import json
from typing import List

from starlette.applications import Starlette
from starlette.responses import HTMLResponse


pagetemplate = """
<!doctype html>
<head>
    <script type="importmap">{imports}</script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script type="text/jsx" data-type="module">
        import React from "react"
        import ReactDOM from "react-dom"
        import ReactMarkdown from "react-markdown"

        const App = () => (
            {root}
        )
        ReactDOM.render(<App />, document.body)
    </script>
</head>
<body style="margin: 0">
    <p>Loading...</p>
</body>

"""

tagtemplate = """
<{name}>
{children}
</{name}>
"""


class Tag:
    def __init__(self, name="", children=None):
        self.name = name
        self.children: List[Tag] = children if children else []

    def __add__(self, obj):
        if isinstance(obj, Tag):
            self.children.append(obj)
        elif isinstance(obj, str):
            tag = Tag("ReactMarkdown", [obj])
            self.children.append(tag)
        return self

    def __str__(self):
        if not self.children:
            return f"<{self.name}/>"
        else:
            return tagtemplate.strip().format(
                name=self.name,
                children="\n".join(str(tag) for tag in self.children),
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        return

    def div(self):
        tag = Tag("div")
        self.children.append(tag)
        return tag

    def ul(self):
        tag = Tag("ul")
        self.children.append(tag)
        return tag

    def ol(self):
        tag = Tag("ol")
        self.children.append(tag)
        return tag

    def li(self):
        tag = Tag("li")
        self.children.append(tag)
        return tag

    def button(self):
        tag = Tag("button")
        self.children.append(tag)
        return tag

    def markdown(self, text):
        tag = Tag("ReactMarkdown", [text])
        self.children.append(tag)
        return tag

    def text(self, text):
        self.children.append(text)


class Page:
    imports = {
        "react": "https://cdn.skypack.dev/react@^v17.0.1",
        "react-dom": "https://cdn.skypack.dev/react-dom@^v17.0.1",
        "react-markdown": "https://cdn.skypack.dev/react-markdown@^v8.0.0",
        "@mantine/core": "https://cdn.skypack.dev/@mantine/core@^v3.6.1",
        "@mantine/hooks": "https://cdn.skypack.dev/@mantine/hooks@^v3.6.1",
    }

    def __init__(self):
        self.root = Tag()

    def __str__(self):
        return pagetemplate.strip().format(
            imports=json.dumps({"imports": self.imports}, indent=2),
            root=str(self.root),
        )


class PageContext:
    def __init__(self, app: Starlette, url: str):
        self.app = app
        self.url = url
        self.page: Page = None

    def __enter__(self):
        self.page = Page()
        return self.page.root

    def __exit__(self, exc_type, exc_value, exc_tb):
        async def handle_get(request):
            return HTMLResponse(str(self.page))

        self.app.add_route(self.url, handle_get)


def page(app: Starlette, url: str):
    return PageContext(app, url)