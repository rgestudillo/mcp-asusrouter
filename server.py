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
    """Fetch all connected devices from the ASUS Router
    
    Retrieves detailed information about each device connected to the router, including:
    - Connection status (connected/disconnected)
    - Device names and MAC addresses
    - Connection type (2.4GHz, 5GHz, wired)
    - IP addresses and assignment method (DHCP/static)
    - Signal strength (RSSI) for wireless connections
    - Connection speeds
    - Time since connection was established
    - Vendor information when available
    
    Returns:
        Dict[str, Any]: A dictionary where keys are device MAC addresses and values contain
                        the connection details for each device
    """
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
    
    This command initiates a full restart of the router. During the reboot process:
    - All network connections will be temporarily interrupted
    - Router configuration settings remain unchanged
    - Any disconnected devices will need to reconnect after reboot
    
    Note: The router will be offline for 1-2 minutes during the reboot.
    
    Returns:
        Dict[str, Any]: A status message confirming the reboot command was sent
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
    """Get detailed wireless network configuration for both 2.4GHz and 5GHz bands
    
    Retrieves comprehensive settings for both wireless networks, including:
    - Network names (SSIDs) and passwords (masked)
    - Security protocols (WPA2-PSK, etc.) and encryption methods (AES)
    - Channel settings and radio status (enabled/disabled)
    - Management Frame Protection (MFP) settings
    - Country code for regulatory compliance
    - Visibility settings (hidden networks)
    - Band-specific configuration details
    
    Returns:
        Dict[str, Any]: A dictionary with nested "2ghz" and "5ghz" configurations
                        containing all wireless settings
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
    Retrieve traffic statistics for all network interfaces
    
    Collects detailed bandwidth usage metrics across all network interfaces, including:
    - Total bytes transferred (sent/received) for all interfaces
    - Current transfer speeds for active connections
    - Separate statistics for WAN, wired LAN, wireless (2.4GHz/5GHz), bridge and USB interfaces
    
    This tool helps monitor network utilization and can identify which interfaces
    are experiencing the most traffic.
    
    Returns:
        Dict[str, Any]: A dictionary with separate entries for each network interface type
                        containing their respective traffic statistics
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
    """Get parental control configuration and rule settings
    
    Retrieves the router's parental control settings, including:
    - Overall activation status (enabled/disabled)
    - Global block status for all devices
    - Defined access control rules for specific devices
    - Time-based restrictions and scheduling information
    
    This tool provides visibility into content filtering and access management
    for devices on the network.
    
    Returns:
        Dict[str, Any]: A dictionary containing the parental control status and any
                        configured access restriction rules
    """
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

@mcp.tool()
async def get_aimesh_info() -> Dict[str, Any]:
    """Get AiMesh system information and node status
    
    Retrieves detailed information about the AiMesh network setup, including:
    - List of all nodes in the mesh network with their status
    - Node details including model, IP address, and firmware version
    - Connection hierarchy (parent-child relationships)
    - Node type (router, repeater) and configuration status
    - Wireless MAC addresses for each node's radios
    
    This tool provides visibility into the entire mesh network topology.
    
    Returns:
        Dict[str, Any]: A dictionary with keys representing node MAC addresses and
                        values containing detailed information about each node
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.AIMESH)
            if data is None:
                return {"message": "No AiMesh data available"}
            return {"aimesh": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information about the router hardware and software
    
    Retrieves detailed system information, including:
    - Hardware specifications (CPU, memory, storage)
    - Model and product identification
    - System uptime and boot information
    - Operating system and kernel details
    - Build version and compilation information
    
    This tool provides a complete overview of the router's hardware and
    software configuration.
    
    Returns:
        Dict[str, Any]: A dictionary containing detailed system information
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.SYSINFO)
            if data is None:
                return {"message": "No system information available"}
            return {"system_info": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_cpu_ram_usage() -> Dict[str, Any]:
    """Get CPU and RAM utilization statistics
    
    Retrieves current resource usage information for the router, including:
    - CPU utilization per core and total usage percentage
    - Available and used memory (RAM) in KB
    - Memory usage percentage
    - Core-specific load information for multi-core processors
    
    This tool helps monitor router performance and identify potential
    resource constraints.
    
    Returns:
        Dict[str, Any]: A dictionary containing separate CPU and RAM utilization metrics
    """
    try:
        router, session = await create_router_connection()
        try:
            cpu_data = await router.async_get_data(AsusData.CPU)
            ram_data = await router.async_get_data(AsusData.RAM)
            return {
                "cpu": cpu_data,
                "ram": ram_data
            }
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_temperature() -> Dict[str, Any]:
    """Get router temperature sensors information
    
    Retrieves temperature readings from various sensors in the router, including:
    - CPU temperature
    - Wireless chipset temperature
    - Additional component temperatures when available
    - Warning thresholds if configured
    
    This tool helps monitor hardware health and identify potential
    overheating issues.
    
    Returns:
        Dict[str, Any]: A dictionary containing temperature readings from available sensors
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.TEMPERATURE)
            if data is None:
                return {"message": "No temperature data available"}
            return {"temperature": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_wan_status() -> Dict[str, Any]:
    """Get detailed WAN (internet) connection status and configuration
    
    Retrieves comprehensive information about the router's internet connection, including:
    - Connection protocol (DHCP, Static, PPPoE)
    - IP address details (public and private)
    - Gateway and DNS server configuration
    - Connection state and link status
    - Lease time remaining for DHCP connections
    - Dual WAN configuration when available
    
    This tool provides complete visibility into the router's internet connectivity.
    
    Returns:
        Dict[str, Any]: A dictionary with detailed WAN connection information
                        including primary and secondary (if configured) interfaces
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.WAN)
            if data is None:
                return {"message": "No WAN data available"}
            return {"wan": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_port_forwarding() -> Dict[str, Any]:
    """Get port forwarding rules and configuration status
    
    Retrieves information about the router's port forwarding setup, including:
    - Overall port forwarding status (enabled/disabled)
    - List of configured port forwarding rules
    - Protocol, port ranges, and target IP addresses for each rule
    - Rule names and descriptions
    
    This tool provides visibility into how external traffic is directed to
    internal devices on the network.
    
    Returns:
        Dict[str, Any]: A dictionary containing the port forwarding status and
                        any configured rules
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.PORT_FORWARDING)
            if data is None:
                return {"message": "No port forwarding data available"}
            return {"port_forwarding": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_vpn_config() -> Dict[str, Any]:
    """Get VPN client and server configuration status
    
    Retrieves information about configured VPN services, including:
    - OpenVPN client connection status (up to 5 profiles)
    - OpenVPN server configuration if enabled
    - WireGuard configuration if supported and enabled
    - Connection error codes if applicable
    
    This tool provides visibility into VPN connectivity status for both
    client and server implementations.
    
    Returns:
        Dict[str, Any]: A dictionary containing separate configuration details for
                        OpenVPN and WireGuard (if available)
    """
    try:
        router, session = await create_router_connection()
        try:
            openvpn_data = await router.async_get_data(AsusData.OPENVPN)
            wireguard_data = await router.async_get_data(AsusData.WIREGUARD)
            return {
                "openvpn": openvpn_data,
                "wireguard": wireguard_data
            }
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_led_status() -> Dict[str, Any]:
    """Get router LED status information
    
    Retrieves the current state of the router's LED indicators:
    - Overall LED status (enabled/disabled)
    - Scheduled LED control settings if configured
    
    This tool can be used to check if the router's LED lights are active
    or have been turned off for less distraction.
    
    Returns:
        Dict[str, Any]: A dictionary containing the current LED status
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.LED)
            if data is None:
                return {"message": "No LED status data available"}
            return {"led": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_firmware_info() -> Dict[str, Any]:
    """Get firmware version information and update availability
    
    Retrieves detailed information about the router's firmware, including:
    - Current installed firmware version
    - Available firmware updates (regular and beta channels)
    - Update check status and configuration
    - Firmware note information if available
    
    This tool helps monitor for available firmware updates and track
    the current firmware version.
    
    Returns:
        Dict[str, Any]: A dictionary containing detailed firmware information
                        and update status
    """
    try:
        router, session = await create_router_connection()
        try:
            firmware = await router.async_get_data(AsusData.FIRMWARE)
            firmware_note = await router.async_get_data(AsusData.FIRMWARE_NOTE)
            return {
                "firmware": firmware,
                "firmware_note": firmware_note
            }
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_dsl_status() -> Dict[str, Any]:
    """Get DSL connection status and line information
    
    Retrieves detailed information about DSL connectivity (for DSL routers), including:
    - Connection status and synchronization state
    - Line statistics (SNR, attenuation, etc.)
    - Data rates (upstream and downstream)
    - DSL standard in use (ADSL, VDSL, etc.)
    - Provider information when available
    
    This tool provides detailed diagnostics for DSL-based internet connections.
    
    Returns:
        Dict[str, Any]: A dictionary containing DSL connection details and line statistics
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.DSL)
            if data is None:
                return {"message": "No DSL data available"}
            return {"dsl": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}