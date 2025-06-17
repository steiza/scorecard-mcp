from typing import Annotated

import httpx
from mcp.server import Server
from mcp.shared.exceptions import McpError
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
)
from pydantic import BaseModel, Field

description = """
Report security best practices and security posture for an open source package or dependency. Fetches OpenSSF Scorecard results and returns a summary of the package's security practices. The information provided is a guideline, and it is up to the user to make a decision about if a package is secure or not.
"""

async def get_scorecard_results(package_name: str) -> str:
    # Attempt to parse the package name
    parsed_package_name = package_name
    if parsed_package_name.endswith('/'):
        parsed_package_name = parsed_package_name[:-1]

    if '/' not in parsed_package_name:
        raise McpError(ErrorData(code=400, message=f"package_name should be of the form platform/owner/repository: {resp}"))

    parts = parsed_package_name.split('/')
    if len(parts) >= 2:
        parsed_package_name = '/'.join(parts[-2:])

    platform = 'github.com'
    if 'gitlab.com' in package_name:
        platform = 'gitlab.com'

    url = f"https://api.scorecard.dev/projects/{platform}/{parsed_package_name}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise McpError(ErrorData(code=resp.status_code, message=f"Failed to fetch scorecard: {resp}"))
        data = resp.json()
        return str(data)

async def serve() -> None:
    server = Server("ossf-scorecard")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="OpenSSF-Scorecard",
                    description=description,
                    inputSchema=OpenSSFScorecard.model_json_schema(),
                )
            ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="OpenSSF-Scorecard",
                description="",
                arguments=[
                    PromptArgument(
                        name="package", description=description, required=True
                    )
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(name, arguments: dict) -> list[TextContent]:
        try:
            args = OpenSSFScorecard(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        package_name = str(args.package_name)
        if not package_name:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="package_name is required"))
        
        content = await get_scorecard_results(package_name)

        return [TextContent(type="text", text=f"OpenSSF Scorecard results for {package_name}:\n{content}")]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        if not arguments or "package_name" not in arguments:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="package_name is required"))

        package_name = arguments["package_name"]

        content = await get_scorecard_results(package_name)
        return GetPromptResult(
            description=f"OpenSSF Scorecard results for {package_name}",
            messages=[
                PromptMessage(
                    role="user", content=TextContent(type="text", text=content)
                )
            ],
        )

    class OpenSSFScorecard(BaseModel):
        package_name: Annotated[
            str,
            Field(
                default="",
                description="Name of package in the form platform/owner/repository. The platform is optional, but if provided should be gitlab.com or github.com. The owner and the repository is supplied by the user.",
            ),
        ]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

def main():
    import asyncio
    asyncio.run(serve())

if __name__ == '__main__':
    main()
