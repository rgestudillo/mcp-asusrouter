import aiohttp
import asyncio
from asusrouter import AsusRouter, AsusData
from asusrouter.modules.state import AsusState
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Tuple, List, Optional
from asusrouter.modules.aura import AsusAura

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

# New additional tools

@mcp.tool()
async def run_speedtest() -> Dict[str, Any]:
    """Run a network speed test from the router
    
    Initiates a speed test directly from the router to measure:
    - Upload speed
    - Download speed
    - Ping time (latency)
    - Jitter
    
    This test can be used to diagnose internet connection performance issues
    without needing to run tests from client devices.
    
    Note: The test may take 30-60 seconds to complete and could briefly impact
    network performance during testing.
    
    Returns:
        Dict[str, Any]: A dictionary containing speed test results including
                        upload and download speeds
    """
    try:
        router, session = await create_router_connection()
        try:
            # Initiate speedtest
            await router.async_run_service("ookla_speedtest", apply=True)
            
            # Wait for test to complete and get results
            # This could take some time, so we'll wait and then fetch the result
            await asyncio.sleep(60)  # Wait for speedtest to complete
            
            # Get the results
            result = await router.async_get_data(AsusData.SPEEDTEST_RESULT)
            if result is None:
                return {"message": "Speed test initiated but no results available yet"}
            return {"speedtest_result": result}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error running speed test: {str(e)}"}

@mcp.tool()
async def set_led_state(state: bool) -> Dict[str, Any]:
    """Turn router LEDs on or off
    
    Controls the LED indicator lights on the router:
    - When off, all indicator lights will be disabled for reduced distraction
    - When on, normal LED operation is restored for status indication
    
    Parameters:
        state (bool): True to turn LEDs on, False to turn them off
    
    Returns:
        Dict[str, Any]: A confirmation message indicating the LED state change
    """
    try:
        router, session = await create_router_connection()
        try:
            # Set LED state
            success = await router.async_set_state(
                AsusState.LED, 
                state=state,
                expect_modify=True
            )
            
            if success:
                return {
                    "message": f"LED state successfully set to: {'ON' if state else 'OFF'}"
                }
            return {"error": "Failed to set LED state"}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error setting LED state: {str(e)}"}

@mcp.tool()
async def set_aura_lighting(effect: str, color: Optional[str] = None, brightness: Optional[int] = None) -> Dict[str, Any]:
    """Control ASUS AURA RGB lighting effects (if supported by router)
    
    Changes the lighting scheme on AURA-enabled ASUS routers:
    - Select from various lighting effects (static, breathing, rainbow, etc.)
    - Control colors for compatible effects
    - Adjust brightness level
    
    Parameters:
        effect (str): Lighting effect to use. Options: "static", "breathing", "rainbow", 
                      "wave", "gradient", "marquee", "off"
        color (Optional[str]): RGB hex color value (e.g., "#ff0000" for red)
        brightness (Optional[int]): Brightness level (0-100)
    
    Returns:
        Dict[str, Any]: A confirmation message indicating the lighting change
    """
    try:
        router, session = await create_router_connection()
        try:
            # Map string effect to AsusAura enum
            effect_map = {
                "static": AsusAura.STATIC,
                "breathing": AsusAura.BREATHING,
                "rainbow": AsusAura.RAINBOW,
                "wave": AsusAura.WAVE,
                "gradient": AsusAura.GRADIENT,
                "marquee": AsusAura.MARQUEE,
                "evolution": AsusAura.EVOLUTION,
                "off": AsusAura.OFF,
                "on": AsusAura.ON
            }
            
            aura_effect = effect_map.get(effect.lower())
            if aura_effect is None:
                return {"error": f"Invalid effect: {effect}. Valid options are: {', '.join(effect_map.keys())}"}
            
            # Process color if provided
            color_rgb = None
            if color and color.startswith("#") and len(color) == 7:
                # Convert from hex (#RRGGBB) to RGB tuple
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                color_rgb = (r, g, b)
            
            # Set AURA state
            kwargs = {}
            if color_rgb:
                kwargs["color"] = color_rgb
            if brightness is not None:
                kwargs["brightness"] = brightness
                
            success = await router.async_set_state(
                AsusState.AURA,
                state=aura_effect,
                expect_modify=True,
                **kwargs
            )
            
            if success:
                return {
                    "message": f"AURA lighting effect set to: {effect}",
                    "details": {
                        "effect": effect,
                        "color": color,
                        "brightness": brightness
                    }
                }
            return {"error": "Failed to set AURA lighting effect"}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error setting AURA lighting: {str(e)}"}

@mcp.tool()
async def get_boottime() -> Dict[str, Any]:
    """Get router boot time and uptime information
    
    Retrieves information about when the router last started and how long
    it has been running, including:
    - Boot timestamp (when the router was last started)
    - Uptime in seconds
    - Human-readable uptime (days, hours, minutes)
    
    This tool is useful for monitoring router stability and determining
    when the last reboot occurred.
    
    Returns:
        Dict[str, Any]: A dictionary with boot time and uptime information
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.BOOTTIME)
            if data is None:
                return {"message": "No boot time data available"}
            return {"boottime": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def set_wifi_settings(band: str, enabled: Optional[bool] = None, ssid: Optional[str] = None, 
                          password: Optional[str] = None, channel: Optional[int] = None) -> Dict[str, Any]:
    """Configure wireless network settings
    
    Modifies the configuration of one of the router's wireless networks:
    - Enable or disable a wireless band
    - Change network name (SSID)
    - Update password
    - Set specific channel
    
    Parameters:
        band (str): WiFi band to configure ("2.4ghz" or "5ghz")
        enabled (Optional[bool]): True to enable the band, False to disable
        ssid (Optional[str]): New network name
        password (Optional[str]): New network password (min 8 characters)
        channel (Optional[int]): Specific channel to use
    
    Returns:
        Dict[str, Any]: A confirmation message with the updated settings
    """
    try:
        router, session = await create_router_connection()
        try:
            # Validate band
            if band not in ["2.4ghz", "5ghz"]:
                return {"error": "Invalid band. Must be '2.4ghz' or '5ghz'"}
            
            # Get current WLAN settings to modify
            current_settings = await router.async_get_data(AsusData.WLAN)
            if not current_settings or band not in current_settings:
                return {"error": f"Could not retrieve current settings for {band} band"}
            
            # Prepare changes
            changes = {}
            band_key = "2ghz" if band == "2.4ghz" else "5ghz"
            
            # Radio enabled/disabled
            if enabled is not None:
                changes[f"{band_key}_radio"] = "1" if enabled else "0"
            
            # SSID
            if ssid is not None:
                changes[f"{band_key}_ssid"] = ssid
            
            # Password (WPA key)
            if password is not None:
                if len(password) < 8:
                    return {"error": "Password must be at least 8 characters"}
                changes[f"{band_key}_wpa_psk"] = password
            
            # Channel
            if channel is not None:
                valid_channels = {
                    "2ghz": list(range(1, 14)),  # Channels 1-13
                    "5ghz": [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]
                }
                
                if channel not in valid_channels[band_key]:
                    return {"error": f"Invalid channel for {band}. Valid channels: {valid_channels[band_key]}"}
                
                changes[f"{band_key}_channel"] = str(channel)
            
            # Apply changes
            if not changes:
                return {"error": "No changes specified"}
            
            # Set WLAN state
            success = await router.async_set_state(
                AsusState.WLAN,
                expect_modify=True,
                **changes
            )
            
            if success:
                return {
                    "message": f"Successfully updated {band} WiFi settings",
                    "updated_settings": changes
                }
            return {"error": "Failed to update WiFi settings"}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error setting WiFi settings: {str(e)}"}

@mcp.tool()
async def get_guest_wifi_status() -> Dict[str, Any]:
    """Get guest WiFi network status and configuration
    
    Retrieves information about the router's guest wireless networks, including:
    - Status (enabled/disabled) for each guest network
    - Network names (SSIDs) and security settings
    - Access restrictions and bandwidth limits
    - Time limitations if configured
    
    This tool provides visibility into guest network configuration for secure
    visitor access management.
    
    Returns:
        Dict[str, Any]: A dictionary containing guest WiFi configuration for
                        both 2.4GHz and 5GHz bands
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.GWLAN)
            if data is None:
                return {"message": "No guest WLAN data available"}
            return {"guest_wifi": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_ports_status() -> Dict[str, Any]:
    """Get physical network port status
    
    Retrieves the status of the router's physical network ports, including:
    - Connection status (connected/disconnected)
    - Port speeds and duplex settings
    - Link aggregation status if applicable
    - Device connected to each port (when available)
    
    This tool provides visibility into which physical ports are in use
    and their current configuration.
    
    Returns:
        Dict[str, Any]: A dictionary containing the status of each physical network port
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.PORTS)
            if data is None:
                return {"message": "No ports data available"}
            return {"ports": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_devicemap() -> Dict[str, Any]:
    """Get comprehensive device map information
    
    Retrieves detailed device classification information, including:
    - Complete device inventory with status information
    - Hardware details for each device and interface
    - Server, client and interface relationships
    - Extended USB device information when available
    
    This tool provides a comprehensive view of all devices connected
    to or part of the router system.
    
    Returns:
        Dict[str, Any]: A detailed map of all devices and interfaces
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.DEVICEMAP)
            if data is None:
                return {"message": "No devicemap data available"}
            return {"devicemap": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}