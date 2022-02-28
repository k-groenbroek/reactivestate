/**
 * Usage: 
 * ./qjs --module mdxcompiler.js component.mdx
 */

import { loadFile } from "std"
import { createProcessor } from "xdm"

const [_, mdxfilepath] = scriptArgs
const content = loadFile(mdxfilepath)
const processor = createProcessor({ jsxRuntime: "classic" })
processor.process(content).then(result => print(result))
