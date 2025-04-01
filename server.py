import aiohttp
from asusrouter import AsusRouter, AsusData
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Tuple

mcp = FastMCP("Asus Router MCP Server", dependencies=["aiohttp", "asusrouter"])

# Router configuration
ROUTER_CONFIG = {
    "hostname": "192.168.72.1",
    "username": "admin",
    "password": "Regina143$#",
    "use_ssl": False
}

# Helper function to create router connection
async def create_router_connection() -> Tuple[AsusRouter, aiohttp.ClientSession]:
    session = aiohttp.ClientSession()   
    router = AsusRouter(
        hostname=ROUTER_CONFIG["hostname"],
        username=ROUTER_CONFIG["username"],
        password=ROUTER_CONFIG["password"],
        use_ssl=ROUTER_CONFIG["use_ssl"],
        session=session
    )
    await router.async_connect()
    return router, session

@mcp.tool()
async def get_connected_devices() -> Dict[str, Any]:
    """Fetch all connected devices from ASUS Router"""
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.CLIENTS)
            if data is None:
                return {"message": "No connected devices data available"}
            return {"devices": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def reboot_router() -> Dict[str, Any]:
    """
    Reboot the ASUS router.
    Note: The router will be offline for 1-2 minutes during the reboot.
    """
    try:
        router, session = await create_router_connection()
        try:
            await router.async_run_service("reboot", apply=True)
            return {
                "message": "Reboot command sent successfully. The router will restart now.",
                "note": "It may take 1-2 minutes for the router to come back online."
            }
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error rebooting router: {str(e)}"}
    
@mcp.tool()
async def get_wlan_status() -> Dict[str, Any]:
    """Get detailed WLAN status information from ASUS Router.
    
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
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.WLAN)
            if data is None:
                return {"message": "No WLAN data available"}
            return {"wlan": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_network_status() -> Dict[str, Any]:
    """
    Retrieve comprehensive network status from the ASUS Router.
    
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
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.NETWORK)
            if data is None:
                return {"message": "No network data available"}
            return {"network": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_parental_control() -> Dict[str, Any]:
    """Get parental control settings from ASUS Router"""
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.PARENTAL_CONTROL)
            if data is None:
                return {"message": "No parental control data available"}
            return {"parental_control": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}
