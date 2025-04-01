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


@mcp.tool()
async def get_network_status() -> Dict[str, Any]:
    """
    Retrieve comprehensive network status from the ASUS Router API.
    
    This function fetches detailed network statistics across different 
    network interfaces and connection types, including:
    - WAN (Wide Area Network)
    - Wired connections
    - Wireless networks (2.4 GHz and 5 GHz bands)
    - Bridge connections
    - USB network interfaces

    Returns:
        Dict[str, Any]: A nested dictionary containing network statistics with the following structure:
        {
            "wan": {
                "rx": int,          # Received bytes
                "tx": int,          # Transmitted bytes
                "rx_speed": float,  # Current receive speed
                "tx_speed": float   # Current transmit speed
            },
            "wired": { ... },       # Similar structure to WAN
            "2ghz": { ... },        # Wireless 2.4 GHz band statistics
            "5ghz": { ... },        # Wireless 5 GHz band statistics
            "bridge": { ... },      # Bridge connection statistics
            "usb": { ... }          # USB network interface statistics
        }

    Raises:
        httpx.RequestError: If there's a network-related error connecting to the router
        httpx.HTTPStatusError: If the router returns an error status code
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("http://0.0.0.0:8000/network")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()


@mcp.tool()
async def get_parental_control() -> Dict[str, Any]:
    """Get parental control settings from ASUS Router API"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://0.0.0.0:8000/parental-control")
        return response.json()
