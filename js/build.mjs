import { build } from "esbuild"

build({
    entryPoints: ["source.js"],
    outfile: "mdxcompiler.js",
    external: ["std"],
    bundle: true,
    minify: true,
    treeShaking: true,
    platform: "browser",
    format: "esm",
})
