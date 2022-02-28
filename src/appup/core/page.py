import json

from starlette.applications import Starlette
from starlette.responses import HTMLResponse


pagetemplate = """
<!doctype html>
<head>
    <script type="importmap">{imports}</script>
    <script type="module">
        import React from "react"
        import ReactDOM from "react-dom"
        import {{ TypographyStylesProvider  }} from "@mantine/core"
        import MDXContent from "./mdx/{mdxfile}"
        const content = React.createElement(MDXContent)
        const app = React.createElement(TypographyStylesProvider, {{}}, content)
        ReactDOM.render(app, document.body)
    </script>
</head>
<body style="margin: 0">
    <p>Loading...</p>
</body>
"""

imports = {
    "react": "https://cdn.skypack.dev/react@^17",
    "react-dom": "https://cdn.skypack.dev/react-dom@^17",
    "@mantine/core": "https://cdn.skypack.dev/@mantine/core@^v3.6.1",
    "@mantine/hooks": "https://cdn.skypack.dev/@mantine/hooks@^v3.6.1",
}


def page(app: Starlette, url: str, mdxfile: str):
    """Add page to app with url."""

    async def handle_get(request):
        content = pagetemplate.strip().format(
            imports=json.dumps({"imports": imports}, indent=2),
            mdxfile=mdxfile,
        )
        return HTMLResponse(content)

    app.add_route(url, handle_get)
