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
    
@mcp.tool()
async def get_wlan_status() -> Dict[str, Any]:
    """Get detailed WLAN status information from ASUS Router API.
    
    This MCP tool provides comprehensive wireless network configuration and status
    information for both 2.4GHz and 5GHz bands of an ASUS router.
    
    Returns:
        Dict[str, Any]: A dictionary containing WLAN status with the following structure:
            {
                "wlan": {
                    "2ghz": {
                        "auth_mode_x": str,  # Authentication mode (e.g., "psk2")
                        "channel": str,      # WiFi channel
                        "ssid": str,         # Network name
                        "radio": bool,       # Whether radio is enabled
                        "crypto": str,       # Encryption type
                        "country_code": str, # Country code for regulations
                        "mfp": str,          # Management Frame Protection status
                        "wpa_psk": str,      # Network password (masked)
                        ...
                    },
                    "5ghz": {
                        # Same structure as 2ghz
                        ...
                    }
                }
            }
    
    Example:
        >>> result = await get_wlan_status()
        >>> print(result["wlan"]["2ghz"]["ssid"])
        'ASUS_38'
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("http://0.0.0.0:8000/wlan")
        return response.json()
