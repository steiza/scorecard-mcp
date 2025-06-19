# scorecard_mcp

[![Install with uvx in VS Code](https://img.shields.io/badge/VS_Code-Install_Scorecard_MCP_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=scorecard&config=%7B%22type%22%3A%20%22stdio%22%2C%20%22command%22%3A%20%22uvx%22%2C%20%22args%22%3A%20%5B%22scorecard-mcp%22%5D%7D)

This is an example [MCP server](https://github.com/modelcontextprotocol/servers/) for [OpenSSF Scorecard](https://scorecard.dev/).

You can use it to ask questions like:

> Is urllib3/urllib3 secure?

That's not an endorsement of asking a LLM with limited context if something is secure, but if users are going to ask they should get back an answer informed by context. A better phrased question would be:

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
