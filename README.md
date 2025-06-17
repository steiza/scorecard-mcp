# scorecard_mcp

This is an example [MCP server](https://github.com/modelcontextprotocol/servers/) for [OpenSSF Scorecard](https://scorecard.dev/).

You can use it to ask questions like:

> Is urllib3/urllib3 secure?

Or:

> What security best practices does node-semver follow?

### Installation

There are several ways to install, depending on what editor you're using; see the [installation instructions on the example `fetch` MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch).

I recommend using:

```
...
    "command": "uxv",
    "args": ["scorecard-mcp"]
...
```

So if you're using Visual Studio Code you'd create a `.vscode/` directory in your project and add a `mcp.json` file that looks like this:

```
{
    "servers": {
        "scorecard": {
            "type": "stdio",
            "command": "uvx",
            "args": ["scorecard-mcp"]
        }
    }
}
```
