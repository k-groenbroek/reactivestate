// Navigate to ui folder
// npx snowpack dev

module.exports = {
    packageOptions: {
        source: "remote",
        types: true,
    },
    buildOptions: {
        watch: true,
        jsxInject: 'import React from "react"',
    }
}
