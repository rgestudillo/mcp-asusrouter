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

@mcp.tool()
async def reboot_router() -> Dict[str, Any]:
    """Reboot the ASUS Router"""
    async with httpx.AsyncClient() as client:
        response = await client.post("http://0.0.0.0:8000/reboot")
        return response.json()