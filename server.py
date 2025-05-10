import aiohttp
import asyncio
from asusrouter import AsusRouter, AsusData
from asusrouter.modules.state import AsusState
from asusrouter.modules.system import AsusSystem # For system service calls
from asusrouter.modules.endpoint import EndpointTools # For ping
from asusrouter.modules.led import AsusLED # For set_led_state
from asusrouter.modules.aura import AsusAura # For set_aura_lighting
from asusrouter.modules.color import ColorRGB # For set_aura_lighting color
from asusrouter.modules.parental_control import AsusBlockAll, AsusParentalControl
from asusrouter.modules.port_forwarding import AsusPortForwarding
from asusrouter.modules.openvpn import AsusOVPNClient, AsusOVPNServer
from asusrouter.modules.wireguard import AsusWireGuardClient, AsusWireGuardServer
from asusrouter.modules.vpnc import AsusVPNC
from asusrouter.modules.wlan import AsusWLAN, Wlan


from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Tuple, List, Optional

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
    """Get detailed wireless network configuration for all supported bands
    
    Retrieves comprehensive settings for all wireless networks (2.4GHz, 5GHz, 5GHz-2, 6GHz if supported), including:
    - Network names (SSIDs) and passwords (masked)
    - Security protocols (WPA2-PSK, etc.) and encryption methods (AES)
    - Channel settings and radio status (enabled/disabled)
    - Management Frame Protection (MFP) settings
    - Country code for regulatory compliance
    - Visibility settings (hidden networks)
    - Band-specific configuration details
    
    Returns:
        Dict[str, Any]: A dictionary with nested entries for each supported band
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
    - Separate statistics for WAN, wired LAN, wireless (2.4GHz/5GHz/etc.), bridge and USB interfaces
    
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
    """Get comprehensive system information about the router hardware and software (SYSINFO)
    
    Retrieves detailed system information, including:
    - WLAN client counts (associated, authenticated, authorized) per band
    - Network connection statistics (total, active)
    - Memory usage details (total, free, buffers, cache, swap, NVRAM, JFFS)
    - CPU load averages (1-min, 5-min, 15-min)
    
    This tool provides a detailed snapshot of the router's current operational status.
    Note: This is different from `get_router_system_status` which refers to `AsusData.SYSTEM`.
    
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
    - Wireless chipset temperature for each band (2.4GHz, 5GHz, etc.)
    - Additional component temperatures when available
    
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
    - Dual WAN configuration when available (mode, priority, aggregation)
    
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
    """Get VPN client and server configuration status for OpenVPN and WireGuard
    
    Retrieves information about configured VPN services, including:
    - OpenVPN client connection status (up to 5 profiles)
    - OpenVPN server configuration if enabled
    - WireGuard client configurations
    - WireGuard server configuration if enabled
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
            # VPN Fusion data could also be relevant
            vpnc_data = await router.async_get_data(AsusData.VPNC)
            return {
                "openvpn": openvpn_data,
                "wireguard": wireguard_data,
                "vpn_fusion": vpnc_data
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
    - Scheduled LED control settings if configured (not directly exposed by AsusData.LED but related)
    
    This tool can be used to check if the router's LED lights are active
    or have been turned off for less distraction.
    
    Returns:
        Dict[str, Any]: A dictionary containing the current LED status (ON/OFF)
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
    - Firmware release note information if available
    
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
    - Line statistics (SNR, attenuation, etc.) (Note: library might only provide data rates)
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
            # Ensure identity is loaded if DSL is conditional
            if not router._identity or router._identity.dsl is None:
                 await router.async_get_identity(force=True)
            
            if router._identity and not router._identity.dsl:
                return {"message": "This router does not support DSL functionality."}

            data = await router.async_get_data(AsusData.DSL)
            if data is None:
                return {"message": "No DSL data available or DSL not supported by this router model."}
            return {"dsl": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

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
    
    Note: The test may take 30-90 seconds to complete and could briefly impact
    network performance during testing.
    
    Returns:
        Dict[str, Any]: A dictionary containing speed test results including
                        upload and download speeds, or a message if results are not yet ready.
    """
    try:
        router, session = await create_router_connection()
        try:
            # Ensure identity is loaded if Ookla is conditional
            if not router._identity or router._identity.ookla is None:
                 await router.async_get_identity(force=True)

            if router._identity and not router._identity.ookla:
                return {"message": "Speedtest (Ookla) is not supported by this router model or firmware."}

            # Initiate speedtest
            # The service name for ookla speedtest might be specific, checking library details.
            # AsusData.SPEEDTEST uses 'ookla_speedtest_get_result', to initiate, it might be 'ookla_speedtest' or similar
            # From system.py, it seems there's no direct `AsusSystem` enum for this.
            # From pyproject.toml & tests, it seems the `ookla_speedtest` service call is correct.
            start_success = await router.async_run_service("ookla_speedtest", apply=True)
            if not start_success:
                return {"error": "Failed to initiate speed test."}
            
            # Wait for test to complete and get results
            # This could take some time, so we'll wait and then fetch the result
            # Giving it a bit more time.
            await asyncio.sleep(75) 
            
            # Get the results
            result = await router.async_get_data(AsusData.SPEEDTEST_RESULT, force=True) # Force to get fresh results
            history = await router.async_get_data(AsusData.SPEEDTEST, force=True) # Get main speedtest data which includes status
            
            if result is None and history and history.get("state") != 0: # 0 often means idle/finished
                 return {"message": f"Speed test initiated. Current status: {history.get('state')}. Results not available yet. Try fetching again in a moment."}
            if result is None:
                return {"message": "Speed test initiated but no results available yet, or test failed to complete."}
                
            return {
                "speedtest_result": result,
                "speedtest_status": history # Includes overall status and config
            }
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error running speed test: {str(e)}"}

@mcp.tool()
async def set_led_state(enable: bool) -> Dict[str, Any]:
    """Turn router LEDs on or off
    
    Controls the LED indicator lights on the router:
    - When off, all indicator lights will be disabled for reduced distraction
    - When on, normal LED operation is restored for status indication
    
    Parameters:
        enable (bool): True to turn LEDs on, False to turn them off
    
    Returns:
        Dict[str, Any]: A confirmation message indicating the LED state change
    """
    try:
        router, session = await create_router_connection()
        try:
            led_asus_state = AsusLED.ON if enable else AsusLED.OFF
            success = await router.async_set_state(
                AsusState.LED, 
                state=led_asus_state, # Use the correct enum member
                expect_modify=True
            )
            
            if success:
                return {
                    "message": f"LED state successfully set to: {'ON' if enable else 'OFF'}"
                }
            return {"error": "Failed to set LED state"}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error setting LED state: {str(e)}"}

@mcp.tool()
async def set_aura_lighting(effect: str, color_hex: Optional[str] = None, brightness: Optional[int] = None) -> Dict[str, Any]:
    """Control ASUS AURA RGB lighting effects (if supported by router)
    
    Changes the lighting scheme on AURA-enabled ASUS routers.
    
    Parameters:
        effect (str): Lighting effect. Options: "static", "breathing", "rainbow", 
                      "wave", "gradient", "marquee", "evolution", "off", "on".
                      "on" will try to restore the previously set effect.
        color_hex (Optional[str]): RGB hex color value (e.g., "#FF0000" for red).
                                 Applicable for effects like static, breathing, gradient, marquee.
        brightness (Optional[int]): Brightness level (0-100, will be scaled to router's range).
                                  Applicable for effects with color support.
    
    Returns:
        Dict[str, Any]: A confirmation message indicating the lighting change.
    """
    try:
        router, session = await create_router_connection()
        try:
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
            
            aura_effect_enum = effect_map.get(effect.lower())
            if aura_effect_enum is None:
                valid_options = ", ".join(effect_map.keys())
                return {"error": f"Invalid effect: '{effect}'. Valid options are: {valid_options}."}
            
            kwargs_for_set_state = {}
            if color_hex:
                if not (color_hex.startswith("#") and len(color_hex) == 7):
                    return {"error": "Invalid color_hex format. Expected '#RRGGBB'."}
                try:
                    r = int(color_hex[1:3], 16)
                    g = int(color_hex[3:5], 16)
                    b = int(color_hex[5:7], 16)
                    # The library expects a ColorRGB object or a tuple for color
                    kwargs_for_set_state["color"] = ColorRGB(r, g, b) 
                except ValueError:
                    return {"error": "Invalid characters in color_hex."}
            
            if brightness is not None:
                if not 0 <= brightness <= 100:
                    return {"error": "Brightness must be between 0 and 100."}
                # The library handles scaling brightness appropriately if it's within a typical 0-100 or 0-255 range.
                # The library's set_brightness in aura.py uses a 0-128 scale internally if not specified.
                # Let's pass it as is, the library should handle it.
                # The `asusrouter.modules.aura.set_brightness` function scales to router's internal representation.
                # It expects brightness 0-128 for asus. So, we might need to scale 0-100 to 0-128.
                # For simplicity, the library likely handles a 0-255 range or its own internal scale.
                # The library's `set_brightness` in `ColorRGBB` uses `self._scale` which defaults to 128.
                # So, if we provide brightness, it's best to scale it to the router's expected range or let the lib do it.
                # The function takes brightness from 0-255 based on HA.
                # Let's assume the library expects 0-255 for brightness when ColorRGB is passed.
                # No, the `set_brightness` in `aura.py` just passes the int along.
                # The ColorRGBB class `set_brightness` method uses `self._scale` (default 128).
                # Let's scale 0-100 to 0-128 for safety.
                scaled_brightness = int((brightness / 100) * 128)
                kwargs_for_set_state["brightness"] = scaled_brightness
                
            success = await router.async_set_state(
                AsusState.AURA,
                state=aura_effect_enum,
                expect_modify=True,
                **kwargs_for_set_state
            )
            
            if success:
                details = {"effect": effect}
                if color_hex: details["color_hex_applied"] = color_hex
                if brightness is not None: details["brightness_requested_0_100"] = brightness
                if "brightness" in kwargs_for_set_state: details["brightness_sent_0_128"] = kwargs_for_set_state["brightness"]
                return {
                    "message": f"AURA lighting effect set to: {effect}",
                    "details": details
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
    - Uptime in seconds (calculated from the timestamp)
    - Human-readable uptime (derived from the timestamp)
    
    This tool is useful for monitoring router stability and determining
    when the last reboot occurred.
    
    Returns:
        Dict[str, Any]: A dictionary with boot time (datetime object) information.
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
    """Configure wireless network settings (SSID, password, channel, enable/disable radio)
    
    Modifies the configuration of one of the router's wireless networks.
    Any parameter not provided will not be changed.
    
    Parameters:
        band (str): WiFi band to configure ("2.4ghz", "5ghz", "5ghz2", "6ghz" - support depends on router model).
        enabled (Optional[bool]): True to enable the radio for this band, False to disable.
        ssid (Optional[str]): New network name (SSID).
        password (Optional[str]): New network password (min 8 characters).
        channel (Optional[int]): Specific channel to use (e.g., 1-13 for 2.4GHz, various for 5/6GHz).
                                 Set to 0 for 'Auto'. Channel validity depends on router region and capabilities.
    
    Returns:
        Dict[str, Any]: A confirmation message with the updated settings or an error message.
    """
    try:
        router, session = await create_router_connection()
        try:
            await router.async_get_identity() # Ensure identity is loaded for wlan list
            if not router._identity or not router._identity.wlan:
                return {"error": "Could not determine router WLAN capabilities."}

            # Map band string to api_id (numeric index)
            # Wlan.FREQ_2G -> 0, Wlan.FREQ_5G -> 1, etc.
            api_id = -1
            target_wlan_enum: Optional[Wlan] = None
            if band.lower() == "2.4ghz": target_wlan_enum = Wlan.FREQ_2G
            elif band.lower() == "5ghz": target_wlan_enum = Wlan.FREQ_5G
            elif band.lower() == "5ghz2": target_wlan_enum = Wlan.FREQ_5G2
            elif band.lower() == "6ghz": target_wlan_enum = Wlan.FREQ_6G
            
            if target_wlan_enum is None:
                return {"error": f"Invalid band: {band}. Supported: '2.4ghz', '5ghz', '5ghz2', '6ghz'."}

            try:
                api_id = router._identity.wlan.index(target_wlan_enum)
            except ValueError:
                 return {"error": f"Band {band} is not supported by this router model."}

            nvram_changes = {}
            if ssid is not None:
                nvram_changes[f"wl{api_id}_ssid"] = ssid
            if password is not None:
                if len(password) < 8:
                    return {"error": "Password must be at least 8 characters."}
                nvram_changes[f"wl{api_id}_wpa_psk"] = password
            if channel is not None:
                # Basic validation, router will ultimately decide if channel is valid for its settings
                if not isinstance(channel, int) or channel < 0:
                     return {"error": "Channel must be a non-negative integer (0 for Auto)."}
                nvram_changes[f"wl{api_id}_channel"] = str(channel) # NVRAM usually stores channel as string
            
            if enabled is not None:
                # This is for radio on/off, which AsusState.WLAN handles differently.
                # To keep this tool cohesive, we'll include it as an NVRAM change too.
                nvram_changes[f"wl{api_id}_radio"] = "1" if enabled else "0"

            if not nvram_changes:
                return {"message": "No changes specified."}
            
            # Service to apply NVRAM changes and restart wireless.
            # 'restart_wireless' is generally used.
            success = await router.async_run_service(
                service="restart_wireless", 
                arguments=nvram_changes,
                apply=True, 
                expect_modify=True 
            )
            
            if success:
                return {
                    "message": f"Successfully requested update for {band} WiFi settings.",
                    "applied_settings": nvram_changes,
                    "note": "Changes may take a moment to apply. Wireless service was restarted."
                }
            return {"error": f"Failed to update {band} WiFi settings."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error setting WiFi settings: {str(e)}"}

@mcp.tool()
async def get_guest_wifi_status() -> Dict[str, Any]:
    """Get guest WiFi network status and configuration for all supported bands
    
    Retrieves information about the router's guest wireless networks, including:
    - Status (enabled/disabled) for each guest network instance per band
    - Network names (SSIDs) and security settings
    - Access restrictions (e.g., LAN access) and bandwidth limits (if configured)
    - Time limitations if configured (e.g., expiration time)
    
    This tool provides visibility into guest network configuration for secure
    visitor access management.
    
    Returns:
        Dict[str, Any]: A dictionary containing guest WiFi configuration for
                        all supported bands and their guest network instances.
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
    """Get physical network port status (LAN, WAN, USB, etc.)
    
    Retrieves the status of the router's physical network ports, including:
    - Connection state (up/down)
    - Current link speed and maximum supported speed
    - Port capabilities (e.g., WAN, LAN, Game port)
    - Information for each AiMesh node's ports if available
    
    This tool provides visibility into which physical ports are in use,
    their current operational status, and capabilities.
    
    Returns:
        Dict[str, Any]: A dictionary containing the status of each physical network port,
                        potentially grouped by device MAC address in an AiMesh setup.
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
    """Get comprehensive device map information (raw data)
    
    Retrieves raw, detailed device classification information from the router's devicemap.
    This includes:
    - WAN status details (primary, secondary if dual WAN)
    - USB device status
    - VPN client/server states (summary level)
    - System uptime string
    - Other low-level status flags and information
    
    This tool provides a low-level, comprehensive view of various router states.
    It's typically more detailed and less processed than other specific `get_` tools.
    
    Returns:
        Dict[str, Any]: A detailed map of various router status points.
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

# --- New Tools Based on Full Library Capabilities ---

@mcp.tool()
async def get_router_flags() -> Dict[str, Any]:
    """Get internal router flags and states.
    
    Retrieves various internal flags set by the router, which might indicate:
    - Reboot pending status
    - Specific service states or errors
    - Other internal operational flags.
    
    This is an advanced tool primarily for debugging or understanding specific
    internal states of the router.
    
    Returns:
        Dict[str, Any]: A dictionary of current router flags.
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.FLAGS)
            if data is None:
                return {"message": "No flags data available."}
            return {"flags": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_vpn_fusion_status() -> Dict[str, Any]:
    """Get VPN Fusion (VPNC) status and configurations.
    
    Retrieves details for all configured VPN Fusion client profiles, including:
    - Profile name and type (OpenVPN, WireGuard, L2TP, PPTP)
    - Connection status (connected, disconnected, error)
    - Assigned VPNC unit ID for control
    - Specific client configuration details (server address, username, etc. - may be masked)
    
    Returns:
        Dict[str, Any]: A dictionary detailing VPN Fusion client profiles and their status.
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.VPNC)
            if data is None:
                return {"message": "No VPN Fusion (VPNC) data available."}
            return {"vpn_fusion_status": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_vpn_fusion_client_list_raw() -> Dict[str, Any]:
    """Get the raw VPN Fusion (VPNC) client list string.
    
    Retrieves the raw string representation of the VPN Fusion client list
    as stored by the router. This is an advanced tool for inspecting the
    exact configuration string.
    
    Returns:
        Dict[str, Any]: A dictionary containing the raw VPNC client list string.
    """
    try:
        router, session = await create_router_connection()
        try:
            data = await router.async_get_data(AsusData.VPNC_CLIENTLIST)
            if data is None:
                return {"message": "No VPN Fusion (VPNC) client list data available."}
            return {"vpnc_clientlist_raw": data}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def ping_host_from_router(host: str, count: int = 4) -> Dict[str, Any]:
    """Ping a specified host from the router itself.
    
    Parameters:
        host (str): The hostname or IP address to ping.
        count (int): Number of ping packets to send (default: 4).
        
    Returns:
        Dict[str, Any]: A dictionary containing the ping results (loss, ping time, jitter)
                        or an error message if the ping command failed.
    """
    try:
        router, session = await create_router_connection()
        try:
            # The `async_api_command` can be used with EndpointTools.NETWORK for ping.
            # The specific command keys might be "act": "ping", "dst_ip": host, "ping_count": str(count)
            # Based on tests/test_data/gt_ax11000pro_stock_388/network_001.content, the result is structured.
            # The library's AsusData.PING uses EndpointTools.NETWORK but doesn't seem to take arguments directly
            # in the `async_get_data` call. We need to use `async_api_command`.
            # The payload structure for `netool.cgi` is typically `act=ping&dst_ip={host}&ping_count={count}`
            
            # Let's assume the library might expose a simpler way or we use the direct command.
            # For now, we will assume the library's `AsusData.PING` could be enhanced or we need a more direct way.
            # The library's `AsusRouter.async_api_command` is suitable here.
            payload = {"act": "ping", "dst_ip": host, "ping_count": str(count)}
            
            # This result will be the raw HTTP response content, which then needs parsing
            # The library's `read` function for `EndpointTools.NETWORK` handles this.
            raw_result = await router.async_api_command(commands=payload, endpoint=EndpointTools.NETWORK)

            # The `process` function for `EndpointTools.NETWORK` just passes the data through.
            # So raw_result should be the final data.
            if raw_result:
                return {"ping_results": raw_result}
            return {"error": "Ping command executed, but no results returned or an error occurred."}

        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error pinging host: {str(e)}"}

@mcp.tool()
async def set_parental_control_block_all(block: bool) -> Dict[str, Any]:
    """Enable or disable the 'Block All Internet Access' feature in Parental Controls.
    
    Parameters:
        block (bool): True to block all internet access, False to disable.
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            block_state = AsusBlockAll.ON if block else AsusBlockAll.OFF
            success = await router.async_set_state(AsusState.BLOCK_ALL, state=block_state, expect_modify=True)
            if success:
                return {"message": f"Parental Controls 'Block All' set to {block}."}
            return {"error": "Failed to set Parental Controls 'Block All' state."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def set_parental_control_global_state(enable: bool) -> Dict[str, Any]:
    """Enable or disable the Parental Controls feature globally.
    
    Parameters:
        enable (bool): True to enable Parental Controls, False to disable.
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            pc_state = AsusParentalControl.ON if enable else AsusParentalControl.OFF
            success = await router.async_set_state(AsusState.PARENTAL_CONTROL, state=pc_state, expect_modify=True)
            if success:
                return {"message": f"Parental Controls global state set to {'enabled' if enable else 'disabled'}."}
            return {"error": "Failed to set Parental Controls global state."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def set_port_forwarding_global_state(enable: bool) -> Dict[str, Any]:
    """Enable or disable Port Forwarding globally.
    
    Parameters:
        enable (bool): True to enable Port Forwarding, False to disable.
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            pf_state = AsusPortForwarding.ON if enable else AsusPortForwarding.OFF
            success = await router.async_set_state(AsusState.PORT_FORWARDING, state=pf_state, expect_modify=True)
            if success:
                return {"message": f"Port Forwarding global state set to {'enabled' if enable else 'disabled'}."}
            return {"error": "Failed to set Port Forwarding global state."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def control_openvpn_client(client_id: int, enable: bool) -> Dict[str, Any]:
    """Enable or disable a specific OpenVPN client profile.
    
    Parameters:
        client_id (int): The ID of the OpenVPN client profile (usually 1-5).
        enable (bool): True to enable (connect) the client, False to disable (disconnect).
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            action = AsusOVPNClient.ON if enable else AsusOVPNClient.OFF
            success = await router.async_set_state(AsusState.OPENVPN_CLIENT, state=action, id=client_id, expect_modify=True)
            if success:
                return {"message": f"OpenVPN client {client_id} set to {'enabled' if enable else 'disabled'}."}
            return {"error": f"Failed to control OpenVPN client {client_id}."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def control_openvpn_server(server_id: int, enable: bool) -> Dict[str, Any]:
    """Enable or disable a specific OpenVPN server profile.
    
    Parameters:
        server_id (int): The ID of the OpenVPN server profile (usually 1-2).
        enable (bool): True to enable the server, False to disable.
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            action = AsusOVPNServer.ON if enable else AsusOVPNServer.OFF
            success = await router.async_set_state(AsusState.OPENVPN_SERVER, state=action, id=server_id, expect_modify=True)
            if success:
                return {"message": f"OpenVPN server {server_id} set to {'enabled' if enable else 'disabled'}."}
            return {"error": f"Failed to control OpenVPN server {server_id}."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def control_wireguard_client(client_id: int, enable: bool) -> Dict[str, Any]:
    """Enable or disable a specific WireGuard client profile.
    
    Parameters:
        client_id (int): The ID of the WireGuard client profile (usually 1-5).
        enable (bool): True to enable (connect) the client, False to disable (disconnect).
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            action = AsusWireGuardClient.ON if enable else AsusWireGuardClient.OFF
            success = await router.async_set_state(AsusState.WIREGUARD_CLIENT, state=action, id=client_id, expect_modify=True)
            if success:
                return {"message": f"WireGuard client {client_id} set to {'enabled' if enable else 'disabled'}."}
            return {"error": f"Failed to control WireGuard client {client_id}."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def control_wireguard_server(server_id: int, enable: bool) -> Dict[str, Any]:
    """Enable or disable a specific WireGuard server profile.
    
    Parameters:
        server_id (int): The ID of the WireGuard server profile (usually 1).
        enable (bool): True to enable the server, False to disable.
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            action = AsusWireGuardServer.ON if enable else AsusWireGuardServer.OFF
            success = await router.async_set_state(AsusState.WIREGUARD_SERVER, state=action, id=server_id, expect_modify=True)
            if success:
                return {"message": f"WireGuard server {server_id} set to {'enabled' if enable else 'disabled'}."}
            return {"error": f"Failed to control WireGuard server {server_id}."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def control_vpn_fusion_client(vpnc_unit_id: int, enable: bool) -> Dict[str, Any]:
    """Enable or disable a specific VPN Fusion client profile using its unit ID.
    
    Parameters:
        vpnc_unit_id (int): The VPNC unit ID of the client profile (obtained from `get_vpn_fusion_status`).
        enable (bool): True to enable (connect) the client, False to disable (disconnect).
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            action = AsusVPNC.ON if enable else AsusVPNC.OFF
            success = await router.async_set_state(AsusState.VPNC, state=action, vpnc_unit=vpnc_unit_id, expect_modify=True)
            if success:
                return {"message": f"VPN Fusion client unit {vpnc_unit_id} set to {'enabled' if enable else 'disabled'}."}
            return {"error": f"Failed to control VPN Fusion client unit {vpnc_unit_id}."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def check_firmware_updates() -> Dict[str, Any]:
    """Trigger a check for new firmware updates on the router.
    
    Returns:
        Dict[str, Any]: A message indicating the check was initiated. 
                        Use `get_firmware_info` to see results after a short delay.
    """
    try:
        router, session = await create_router_connection()
        try:
            success = await router.async_set_state(AsusState.SYSTEM, state=AsusSystem.FIRMWARE_CHECK)
            if success:
                return {"message": "Firmware update check initiated. Use get_firmware_info to see results after a moment."}
            return {"error": "Failed to initiate firmware update check."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def start_firmware_upgrade() -> Dict[str, Any]:
    """Initiate a firmware upgrade if an update is available.
    
    The router will download and install the latest available firmware.
    This process will involve a reboot and network downtime.
    
    Returns:
        Dict[str, Any]: A message indicating the upgrade process was initiated.
    """
    try:
        router, session = await create_router_connection()
        try:
            success = await router.async_set_state(AsusState.SYSTEM, state=AsusSystem.FIRMWARE_UPGRADE)
            if success:
                return {"message": "Firmware upgrade process initiated. The router will download, install, and reboot."}
            return {"error": "Failed to initiate firmware upgrade. Ensure an update is available via get_firmware_info."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def rebuild_aimesh_network() -> Dict[str, Any]:
    """Trigger a rebuild of the AiMesh network.
    
    This can help resolve connectivity issues between AiMesh nodes.
    May cause temporary network interruptions.
    
    Returns:
        Dict[str, Any]: Confirmation that the AiMesh rebuild process was initiated.
    """
    try:
        router, session = await create_router_connection()
        try:
            success = await router.async_set_state(AsusState.SYSTEM, state=AsusSystem.AIMESH_REBUILD)
            if success:
                return {"message": "AiMesh network rebuild initiated."}
            return {"error": "Failed to initiate AiMesh network rebuild."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def restart_dns_service() -> Dict[str, Any]:
    """Restart the DNS service (dnsmasq) on the router.
    
    This can help resolve DNS-related issues.
    
    Returns:
        Dict[str, Any]: Confirmation that the DNS service restart was initiated.
    """
    try:
        router, session = await create_router_connection()
        try:
            success = await router.async_set_state(AsusState.SYSTEM, state=AsusSystem.RESTART_DNSMASQ)
            if success:
                return {"message": "DNS service (dnsmasq) restart initiated."}
            return {"error": "Failed to initiate DNS service restart."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def restart_httpd_service() -> Dict[str, Any]:
    """Restart the router's web server (HTTPD).
    
    This can help if the router's web interface becomes unresponsive.
    Access to the web UI will be briefly interrupted.
    
    Returns:
        Dict[str, Any]: Confirmation that the HTTPD service restart was initiated.
    """
    try:
        router, session = await create_router_connection()
        try:
            success = await router.async_set_state(AsusState.SYSTEM, state=AsusSystem.RESTART_HTTPD)
            if success:
                return {"message": "Router web server (HTTPD) restart initiated."}
            return {"error": "Failed to initiate HTTPD service restart."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def set_wifi_radio_state(band: str, enable: bool) -> Dict[str, Any]:
    """Enable or disable the radio for a specific WiFi band.
    
    Parameters:
        band (str): WiFi band to control ("2.4ghz", "5ghz", "5ghz2", "6ghz").
                    Support depends on router model.
        enable (bool): True to enable the radio, False to disable.
        
    Returns:
        Dict[str, Any]: Confirmation of the action.
    """
    try:
        router, session = await create_router_connection()
        try:
            await router.async_get_identity() # Ensure identity is loaded for wlan list
            if not router._identity or not router._identity.wlan:
                return {"error": "Could not determine router WLAN capabilities."}

            api_id = -1
            target_wlan_enum: Optional[Wlan] = None
            band_lower = band.lower()
            if band_lower == "2.4ghz": target_wlan_enum = Wlan.FREQ_2G
            elif band_lower == "5ghz": target_wlan_enum = Wlan.FREQ_5G
            elif band_lower == "5ghz2": target_wlan_enum = Wlan.FREQ_5G2
            elif band_lower == "6ghz": target_wlan_enum = Wlan.FREQ_6G
            
            if target_wlan_enum is None:
                return {"error": f"Invalid band: {band}. Supported: '2.4ghz', '5ghz', '5ghz2', '6ghz'."}

            try:
                api_id = router._identity.wlan.index(target_wlan_enum)
            except ValueError:
                 return {"error": f"Band {band} is not supported by this router model."}

            wlan_state = AsusWLAN.ON if enable else AsusWLAN.OFF
            
            success = await router.async_set_state(
                AsusState.WLAN,
                state=wlan_state,
                api_type="wlan", # This parameter is expected by the wlan.set_state module
                api_id=api_id,
                expect_modify=True
            )
            
            if success:
                return {"message": f"WiFi radio for {band} set to {'enabled' if enable else 'disabled'}."}
            return {"error": f"Failed to set WiFi radio state for {band}."}
        finally:
            await router.async_disconnect()
            await session.close()
    except Exception as e:
        return {"error": f"Error setting WiFi radio state: {str(e)}"}

# Main execution for testing (optional)
if __name__ == "__main__":
    # To test a specific tool:
    # async def main_test():
    #     result = await get_connected_devices()
    #     print(result)
    # asyncio.run(main_test())
    
    # To run the MCP server (if you were to serve these tools via FastMCP)
    # mcp.run() # This would typically be in your main server script
    print("Asus Router MCP tools defined. Run with `mcp.run()` in your main server script.")
