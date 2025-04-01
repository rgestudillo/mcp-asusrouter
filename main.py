import httpx
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

mcp = FastMCP("KASHI THESIS")


@mcp.tool()
async def get_connected_devices() -> Dict[str, Any]:
    """Fetch all connected devices from ASUS Router API"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://0.0.0.0:8000/devices")
        return response.json()
