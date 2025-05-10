import aiohttp
import asyncio
from asusrouter import AsusRouter, AsusData
from asusrouter.modules.state import AsusState
from asusrouter.modules.system import AsusSystem
from asusrouter.modules.led import AsusLED
from asusrouter.modules.aura import AsusAura
from asusrouter.modules.wlan import AsusWLAN
from asusrouter.modules.parental_control import AsusParentalControl, AsusBlockAll
from asusrouter.modules.port_forwarding import AsusPortForwarding, PortForwardingRule
from asusrouter.modules.openvpn import AsusOVPNServer, AsusOVPNClient
from asusrouter.modules.wireguard import AsusWireGuardServer, AsusWireGuardClient
from asusrouter.modules.vpnc import AsusVPNC
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Tuple, List, Optional, Union, cast

from mcp.server.fastmcp import FastMCP

# Router configuration
ROUTER_CONFIG = {
    "hostname": "192.168.72.1",
    "username": "admin",
    "password": "Regina143$#",
    "use_ssl": False
}

# Router helper class to manage the router connection
class RouterHelper:
    def __init__(self):
        self.router: Optional[AsusRouter] = None
        self._lock = asyncio.Lock()
        
    async def get_router(self) -> AsusRouter:
        """Get or create an AsusRouter instance."""
        async with self._lock:
            if self.router is None or not self.router.connected:
                self.router = AsusRouter(
                    hostname=ROUTER_CONFIG["hostname"],
                    username=ROUTER_CONFIG["username"],
                    password=ROUTER_CONFIG["password"],
                    use_ssl=ROUTER_CONFIG["use_ssl"]
                )
                await self.router.async_connect()
            return self.router
        
    async def close(self):
        """Clean up router connections."""
        if self.router:
            await self.router.async_cleanup()
            self.router = None
            
# Create a global router helper instance
router_helper = RouterHelper()


# Create the MCP server
mcp = FastMCP("Asus Router MCP Server", dependencies=["aiohttp", "asusrouter"])

# Data retrieval functions - each one maps to an AsusData enum

# Connectivity management tools
@mcp.tool(description="Establish a connection to the router and get its identity")
async def connect_to_router() -> Dict[str, Any]:
    """Connect to the Asus Router and retrieve its identity information."""
    router = await router_helper.get_router()
    identity = await router.async_get_identity(force=True)
    return {
        "connected": router.connected,
        "model": identity.model,
        "product_id": identity.product_id,
        "serial": identity.serial,
        "mac": identity.mac,
        "firmware": str(identity.firmware) if identity.firmware else None,
        "is_merlin": identity.merlin,
        "features": {
            "aimesh": identity.aimesh,
            "aura": identity.aura,
            "aura_zone": identity.aura_zone,
            "dsl": identity.dsl,
            "led": identity.led,
            "ookla": identity.ookla,
            "vpn_status": identity.vpn_status
        },
        "services": identity.services
    }

@mcp.tool(description="Disconnect from the router")
async def disconnect_from_router() -> Dict[str, bool]:
    """Disconnect from the router and release resources."""
    if router_helper.router:
        await router_helper.router.async_disconnect()
        await router_helper.close()
        return {"disconnected": True}
    return {"disconnected": False}

@mcp.tool(description="Get router identity information")
async def get_router_identity() -> Dict[str, Any]:
    """Get detailed identity information about the router."""
    router = await router_helper.get_router()
    identity = await router.async_get_identity(force=True)
    return {
        "model": identity.model,
        "product_id": identity.product_id,
        "serial": identity.serial,
        "mac": identity.mac,
        "lan_mac": getattr(identity, "lan_mac", None),
        "wan_mac": getattr(identity, "wan_mac", None),
        "firmware": str(identity.firmware) if identity.firmware else None,
        "is_merlin": identity.merlin,
        "features": {
            "aimesh": identity.aimesh,
            "aura": identity.aura,
            "aura_zone": identity.aura_zone,
            "dsl": identity.dsl,
            "led": identity.led,
            "ookla": identity.ookla,
            "vpn_status": identity.vpn_status
        },
        "services": identity.services,
        "wlan": [{"band": w.band, "type": w.type.name, "mac": w.mac} for w in identity.wlan] if identity.wlan else []
    }

# Data retrieval tools - one for each AsusData type
@mcp.tool(description="Get AiMesh information and status")
async def get_aimesh_data() -> Dict[str, Any]:
    """Get information about the AiMesh network topology and status."""
    router = await router_helper.get_router()
    aimesh_data = await router.async_get_data(AsusData.AIMESH)
    return aimesh_data

@mcp.tool(description="Get Aura RGB lighting status")
async def get_aura_data() -> Dict[str, Any]:
    """Get Aura RGB lighting settings and status."""
    router = await router_helper.get_router()
    aura_data = await router.async_get_data(AsusData.AURA)
    return aura_data

@mcp.tool(description="Get router boot time information")
async def get_boottime_data() -> Dict[str, Any]:
    """Get the router's boot time and calculate uptime."""
    router = await router_helper.get_router()
    boottime_data = await router.async_get_data(AsusData.BOOTTIME)
    
    # Add uptime information
    if isinstance(boottime_data, dict) and "boottime" in boottime_data:
        boot_timestamp = boottime_data.get("boottime")
        if boot_timestamp:
            current_time = datetime.now(timezone.utc)
            boot_time = datetime.fromtimestamp(boot_timestamp, timezone.utc)
            uptime = current_time - boot_time
            boottime_data["uptime_seconds"] = uptime.total_seconds()
            boottime_data["uptime_human"] = str(timedelta(seconds=int(uptime.total_seconds())))
    
    return boottime_data

@mcp.tool(description="Get information about all clients connected to the router")
async def get_clients_data() -> Dict[str, Any]:
    """Get detailed information about all clients connected to the router network."""
    router = await router_helper.get_router()
    clients_data = await router.async_get_data(AsusData.CLIENTS)
    return clients_data

@mcp.tool(description="Get CPU usage statistics")
async def get_cpu_data() -> Dict[str, Any]:
    """Get CPU usage statistics from the router."""
    router = await router_helper.get_router()
    cpu_data = await router.async_get_data(AsusData.CPU)
    return cpu_data

@mcp.tool(description="Get device map information")
async def get_devicemap_data() -> Dict[str, Any]:
    """Get the device map with low-level details about connected devices."""
    router = await router_helper.get_router()
    devicemap_data = await router.async_get_data(AsusData.DEVICEMAP)
    return devicemap_data

@mcp.tool(description="Get DSL connection statistics")
async def get_dsl_data() -> Dict[str, Any]:
    """Get DSL connection information and statistics (for DSL routers)."""
    router = await router_helper.get_router()
    dsl_data = await router.async_get_data(AsusData.DSL)
    return dsl_data

@mcp.tool(description="Get firmware information")
async def get_firmware_data() -> Dict[str, Any]:
    """Get firmware version and update availability information."""
    router = await router_helper.get_router()
    firmware_data = await router.async_get_data(AsusData.FIRMWARE)
    return firmware_data

@mcp.tool(description="Get firmware release notes")
async def get_firmware_note_data() -> Dict[str, Any]:
    """Get firmware release notes for available updates."""
    router = await router_helper.get_router()
    firmware_note_data = await router.async_get_data(AsusData.FIRMWARE_NOTE)
    return firmware_note_data

@mcp.tool(description="Get router internal flags")
async def get_flags_data() -> Dict[str, Any]:
    """Get internal router flags and state information."""
    router = await router_helper.get_router()
    flags_data = await router.async_get_data(AsusData.FLAGS)
    return flags_data

@mcp.tool(description="Get guest WLAN information")
async def get_gwlan_data() -> Dict[str, Any]:
    """Get guest wireless network configuration and status."""
    router = await router_helper.get_router()
    gwlan_data = await router.async_get_data(AsusData.GWLAN)
    return gwlan_data

@mcp.tool(description="Get LED status")
async def get_led_data() -> Dict[str, Any]:
    """Get the current LED status of the router."""
    router = await router_helper.get_router()
    led_data = await router.async_get_data(AsusData.LED)
    return led_data

@mcp.tool(description="Get network statistics")
async def get_network_data() -> Dict[str, Any]:
    """Get detailed network statistics for all interfaces."""
    router = await router_helper.get_router()
    network_data = await router.async_get_data(AsusData.NETWORK)
    return network_data

@mcp.tool(description="Get AiMesh node information")
async def get_node_info_data() -> Dict[str, Any]:
    """Get information about AiMesh nodes in the network."""
    router = await router_helper.get_router()
    node_info_data = await router.async_get_data(AsusData.NODE_INFO)
    return node_info_data

@mcp.tool(description="Get OpenVPN status")
async def get_openvpn_data() -> Dict[str, Any]:
    """Get OpenVPN configuration and status information."""
    router = await router_helper.get_router()
    openvpn_data = await router.async_get_data(AsusData.OPENVPN)
    return openvpn_data

@mcp.tool(description="Get OpenVPN client status")
async def get_openvpn_client_data() -> Dict[str, Any]:
    """Get OpenVPN client configuration and status information."""
    router = await router_helper.get_router()
    openvpn_client_data = await router.async_get_data(AsusData.OPENVPN_CLIENT)
    return openvpn_client_data

@mcp.tool(description="Get OpenVPN server status")
async def get_openvpn_server_data() -> Dict[str, Any]:
    """Get OpenVPN server configuration and status information."""
    router = await router_helper.get_router()
    openvpn_server_data = await router.async_get_data(AsusData.OPENVPN_SERVER)
    return openvpn_server_data

@mcp.tool(description="Get parental control settings")
async def get_parental_control_data() -> Dict[str, Any]:
    """Get parental control configuration and rules."""
    router = await router_helper.get_router()
    parental_control_data = await router.async_get_data(AsusData.PARENTAL_CONTROL)
    return parental_control_data

@mcp.tool(description="Perform a ping test from the router")
async def get_ping_data(host: str = "google.com") -> Dict[str, Any]:
    """Perform a ping test from the router to a specified host."""
    router = await router_helper.get_router()
    ping_data = await router.async_get_data(AsusData.PING, request={"address": host})
    return ping_data

@mcp.tool(description="Get port forwarding rules")
async def get_port_forwarding_data() -> Dict[str, Any]:
    """Get port forwarding rules configured on the router."""
    router = await router_helper.get_router()
    port_forwarding_data = await router.async_get_data(AsusData.PORT_FORWARDING)
    return port_forwarding_data

@mcp.tool(description="Get Ethernet port status")
async def get_ports_data() -> Dict[str, Any]:
    """Get the status of physical Ethernet ports on the router."""
    router = await router_helper.get_router()
    ports_data = await router.async_get_data(AsusData.PORTS)
    return ports_data

@mcp.tool(description="Get RAM usage statistics")
async def get_ram_data() -> Dict[str, Any]:
    """Get RAM usage statistics from the router."""
    router = await router_helper.get_router()
    ram_data = await router.async_get_data(AsusData.RAM)
    return ram_data

@mcp.tool(description="Get speedtest results")
async def get_speedtest_data() -> Dict[str, Any]:
    """Get router's built-in speedtest configuration and results."""
    router = await router_helper.get_router()
    speedtest_data = await router.async_get_data(AsusData.SPEEDTEST)
    return speedtest_data

@mcp.tool(description="Get detailed speedtest result")
async def get_speedtest_result_data() -> Dict[str, Any]:
    """Get detailed results from the router's built-in speedtest."""
    router = await router_helper.get_router()
    speedtest_result_data = await router.async_get_data(AsusData.SPEEDTEST_RESULT)
    return speedtest_result_data

@mcp.tool(description="Get system information")
async def get_sysinfo_data() -> Dict[str, Any]:
    """Get comprehensive system information including CPU, memory, and load averages."""
    router = await router_helper.get_router()
    sysinfo_data = await router.async_get_data(AsusData.SYSINFO)
    return sysinfo_data

@mcp.tool(description="Get system-level status")
async def get_system_data() -> Dict[str, Any]:
    """Get system-level status information."""
    router = await router_helper.get_router()
    system_data = await router.async_get_data(AsusData.SYSTEM)
    return system_data

@mcp.tool(description="Get temperature readings")
async def get_temperature_data() -> Dict[str, Any]:
    """Get temperature readings from various sensors in the router."""
    router = await router_helper.get_router()
    temperature_data = await router.async_get_data(AsusData.TEMPERATURE)
    return temperature_data

@mcp.tool(description="Get VPN Fusion (VPNC) status")
async def get_vpnc_data() -> Dict[str, Any]:
    """Get VPN Fusion (VPNC) configuration and status information."""
    router = await router_helper.get_router()
    vpnc_data = await router.async_get_data(AsusData.VPNC)
    return vpnc_data

@mcp.tool(description="Get VPNC client list")
async def get_vpnc_clientlist_data() -> Dict[str, Any]:
    """Get VPN Fusion client list and configuration information."""
    router = await router_helper.get_router()
    vpnc_clientlist_data = await router.async_get_data(AsusData.VPNC_CLIENTLIST)
    return vpnc_clientlist_data

@mcp.tool(description="Get WAN connection status")
async def get_wan_data() -> Dict[str, Any]:
    """Get WAN (Internet) connection configuration and status information."""
    router = await router_helper.get_router()
    wan_data = await router.async_get_data(AsusData.WAN)
    return wan_data

@mcp.tool(description="Get WireGuard VPN status")
async def get_wireguard_data() -> Dict[str, Any]:
    """Get WireGuard VPN configuration and status information."""
    router = await router_helper.get_router()
    wireguard_data = await router.async_get_data(AsusData.WIREGUARD)
    return wireguard_data

@mcp.tool(description="Get WireGuard client status")
async def get_wireguard_client_data() -> Dict[str, Any]:
    """Get WireGuard client configuration and status information."""
    router = await router_helper.get_router()
    wireguard_client_data = await router.async_get_data(AsusData.WIREGUARD_CLIENT)
    return wireguard_client_data

@mcp.tool(description="Get WireGuard server status")
async def get_wireguard_server_data() -> Dict[str, Any]:
    """Get WireGuard server configuration and status information."""
    router = await router_helper.get_router()
    wireguard_server_data = await router.async_get_data(AsusData.WIREGUARD_SERVER)
    return wireguard_server_data

@mcp.tool(description="Get WLAN (WiFi) status and configuration")
async def get_wlan_data() -> Dict[str, Any]:
    """Get wireless network configuration and status information."""
    router = await router_helper.get_router()
    wlan_data = await router.async_get_data(AsusData.WLAN)
    return wlan_data

# System control functions - based on AsusSystem enum values
@mcp.tool(description="Reboot the router")
async def reboot_router() -> Dict[str, Any]:
    """Reboot the router. This will cause the router to restart completely."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.REBOOT)
    return {"success": result, "action": "reboot", "message": "Router reboot initiated"}

@mcp.tool(description="Restart AiMesh network")
async def restart_aimesh() -> Dict[str, Any]:
    """Restart the entire AiMesh network (main router and all nodes)."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.AIMESH_REBOOT)
    return {"success": result, "action": "restart_aimesh", "message": "AiMesh restart initiated"}

@mcp.tool(description="Rebuild AiMesh network topology")
async def rebuild_aimesh() -> Dict[str, Any]:
    """Rebuild the AiMesh network topology, reconnecting all nodes."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.AIMESH_REBUILD)
    return {"success": result, "action": "rebuild_aimesh", "message": "AiMesh rebuild initiated"}

@mcp.tool(description="Restart Aura RGB lighting")
async def restart_aura_rgb() -> Dict[str, Any]:
    """Restart the Aura RGB lighting system on the router."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.AURA_RESTART)
    return {"success": result, "action": "restart_aura_rgb", "message": "Aura RGB restart initiated"}

@mcp.tool(description="Check for firmware updates")
async def check_firmware_updates() -> Dict[str, Any]:
    """Check if any firmware updates are available for the router."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.FIRMWARE_CHECK)
    return {"success": result, "action": "check_firmware", "message": "Firmware check initiated"}

@mcp.tool(description="Upgrade router firmware")
async def upgrade_firmware() -> Dict[str, Any]:
    """Upgrade the router firmware if an update is available."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.FIRMWARE_UPGRADE)
    return {"success": result, "action": "upgrade_firmware", "message": "Firmware upgrade initiated"}

@mcp.tool(description="Start firmware upgrade process")
async def start_firmware_upgrade() -> Dict[str, Any]:
    """Start the firmware upgrade process on the router."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.UPGRADE_START)
    return {"success": result, "action": "start_upgrade", "message": "Firmware upgrade started"}

@mcp.tool(description="Stop firmware upgrade process")
async def stop_firmware_upgrade() -> Dict[str, Any]:
    """Stop the firmware upgrade process if it's in progress."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.UPGRADE_STOP)
    return {"success": result, "action": "stop_upgrade", "message": "Firmware upgrade stopped"}

@mcp.tool(description="Restart and upgrade firmware")
async def restart_and_upgrade_firmware() -> Dict[str, Any]:
    """Restart the router and upgrade the firmware."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.UPGRADE_RESTART)
    return {"success": result, "action": "restart_upgrade", "message": "Restart and upgrade initiated"}

@mcp.tool(description="Restart firewall service")
async def restart_firewall() -> Dict[str, Any]:
    """Restart the router's firewall service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_FIREWALL)
    return {"success": result, "action": "restart_firewall", "message": "Firewall restart initiated"}

@mcp.tool(description="Restart web server (HTTP daemon)")
async def restart_web_server() -> Dict[str, Any]:
    """Restart the router's web server (HTTP daemon) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_HTTPD)
    return {"success": result, "action": "restart_httpd", "message": "Web server restart initiated"}

@mcp.tool(description="Restart Samba file sharing service")
async def restart_samba() -> Dict[str, Any]:
    """Restart the router's Samba file sharing service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_SAMBA)
    return {"success": result, "action": "restart_samba", "message": "Samba restart initiated"}

@mcp.tool(description="Restart WAN connection")
async def restart_wan(wan_id: int = 0) -> Dict[str, Any]:
    """Restart the router's WAN (internet) connection. Optionally specify a WAN ID (default: 0)."""
    router = await router_helper.get_router()
    # For WAN services, we may need to append the WAN ID
    service = f"{AsusSystem.RESTART_WAN}" + (f"{wan_id}" if wan_id > 0 else "")
    result = await router.async_run_service(service)
    return {"success": result, "action": "restart_wan", "wan_id": wan_id, "message": f"WAN {wan_id} restart initiated"}

@mcp.tool(description="Restart all wireless interfaces")
async def restart_wireless() -> Dict[str, Any]:
    """Restart all wireless (WiFi) interfaces on the router."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_WIRELESS)
    return {"success": result, "action": "restart_wireless", "message": "Wireless interfaces restart initiated"}

@mcp.tool(description="Restart OpenVPN daemon")
async def restart_openvpn() -> Dict[str, Any]:
    """Restart the router's OpenVPN daemon service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_OPENVPND)
    return {"success": result, "action": "restart_openvpn", "message": "OpenVPN daemon restart initiated"}

@mcp.tool(description="Restart WireGuard service")
async def restart_wireguard() -> Dict[str, Any]:
    """Restart the router's WireGuard VPN service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_WGS)
    return {"success": result, "action": "restart_wireguard", "message": "WireGuard service restart initiated"}

@mcp.tool(description="Restart UPnP service")
async def restart_upnp() -> Dict[str, Any]:
    """Restart the router's Universal Plug and Play (UPnP) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_UPNP)
    return {"success": result, "action": "restart_upnp", "message": "UPnP service restart initiated"}

@mcp.tool(description="Restart DNS service")
async def restart_dns() -> Dict[str, Any]:
    """Restart the router's DNS (dnsmasq) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_DNSMASQ)
    return {"success": result, "action": "restart_dns", "message": "DNS service restart initiated"}

@mcp.tool(description="Restart DNS Filter service")
async def restart_dnsfilter() -> Dict[str, Any]:
    """Restart the router's DNS filter service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_DNSFILTER)
    return {"success": result, "action": "restart_dnsfilter", "message": "DNS filter service restart initiated"}

@mcp.tool(description="Restart time synchronization service")
async def restart_time_service() -> Dict[str, Any]:
    """Restart the router's time synchronization service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_TIME)
    return {"success": result, "action": "restart_time", "message": "Time service restart initiated"}

@mcp.tool(description="Restart FTP server")
async def restart_ftp() -> Dict[str, Any]:
    """Restart the router's FTP server service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_FTPD)
    return {"success": result, "action": "restart_ftp", "message": "FTP server restart initiated"}

@mcp.tool(description="Restart router LEDs")
async def restart_leds() -> Dict[str, Any]:
    """Restart the router's LED service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_LEDS)
    return {"success": result, "action": "restart_leds", "message": "LEDs restart initiated"}

@mcp.tool(description="Reset router LED state")
async def reset_led() -> Dict[str, Any]:
    """Reset the router's LED state to default."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESET_LED)
    return {"success": result, "action": "reset_led", "message": "LED reset initiated"}

@mcp.tool(description="Restart cloud sync service")
async def restart_cloud_sync() -> Dict[str, Any]:
    """Restart the router's AiCloud 2.0 sync service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_CLOUDSYNC)
    return {"success": result, "action": "restart_cloudsync", "message": "Cloud sync restart initiated"}

@mcp.tool(description="Restart captive portal")
async def restart_captive_portal() -> Dict[str, Any]:
    """Restart the router's captive portal service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_CP)
    return {"success": result, "action": "restart_cp", "message": "Captive portal restart initiated"}

@mcp.tool(description="Restart DDNS service")
async def restart_ddns() -> Dict[str, Any]:
    """Restart the router's Dynamic DNS service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_DDNS_LE)
    return {"success": result, "action": "restart_ddns", "message": "DDNS service restart initiated"}

@mcp.tool(description="Restart disk monitor service")
async def restart_disk_monitor() -> Dict[str, Any]:
    """Restart the router's disk monitor service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_DISKMON)
    return {"success": result, "action": "restart_diskmon", "message": "Disk monitor restart initiated"}

@mcp.tool(description="Start disk format")
async def start_disk_format() -> Dict[str, Any]:
    """Start the disk format process for attached storage devices."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.START_DISKFORMAT)
    return {"success": result, "action": "start_diskformat", "message": "Disk format started"}

@mcp.tool(description="Start disk scan")
async def start_disk_scan() -> Dict[str, Any]:
    """Start a disk scan for attached storage devices."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.START_DISKSCAN)
    return {"success": result, "action": "start_diskscan", "message": "Disk scan started"}

@mcp.tool(description="Restart QoS service")
async def restart_qos() -> Dict[str, Any]:
    """Restart the router's Quality of Service (QoS) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_QOS)
    return {"success": result, "action": "restart_qos", "message": "QoS service restart initiated"}

@mcp.tool(description="Restart VPN Fusion service")
async def restart_vpnc() -> Dict[str, Any]:
    """Restart the router's VPN Fusion (VPNC) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_VPNC)
    return {"success": result, "action": "restart_vpnc", "message": "VPN Fusion restart initiated"}

@mcp.tool(description="Stop VPN Fusion service")
async def stop_vpnc() -> Dict[str, Any]:
    """Stop the router's VPN Fusion (VPNC) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.STOP_VPNC)
    return {"success": result, "action": "stop_vpnc", "message": "VPN Fusion stop initiated"}

@mcp.tool(description="Restart legacy VPN daemon")
async def restart_vpnd() -> Dict[str, Any]:
    """Restart the router's legacy VPN daemon service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_VPND)
    return {"success": result, "action": "restart_vpnd", "message": "Legacy VPN daemon restart initiated"}

@mcp.tool(description="Stop legacy VPN daemon")
async def stop_vpnd() -> Dict[str, Any]:
    """Stop the router's legacy VPN daemon service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.STOP_VPND)
    return {"success": result, "action": "stop_vpnd", "message": "Legacy VPN daemon stop initiated"}

@mcp.tool(description="Stop OpenVPN server")
async def stop_openvpn() -> Dict[str, Any]:
    """Stop the router's OpenVPN server service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.STOP_OPENVPND)
    return {"success": result, "action": "stop_openvpn", "message": "OpenVPN server stop initiated"}

@mcp.tool(description="Restart WebDAV service")
async def restart_webdav() -> Dict[str, Any]:
    """Restart the router's WebDAV service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_WEBDAV)
    return {"success": result, "action": "restart_webdav", "message": "WebDAV service restart initiated"}

@mcp.tool(description="Restart subnet")
async def restart_subnet() -> Dict[str, Any]:
    """Restart the router's subnet service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_SUBNET)
    return {"success": result, "action": "restart_subnet", "message": "Subnet restart initiated"}

@mcp.tool(description="Restart Time Machine backup service")
async def restart_time_machine() -> Dict[str, Any]:
    """Restart the router's Time Machine backup service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_TIMEMACHINE)
    return {"success": result, "action": "restart_timemachine", "message": "Time Machine service restart initiated"}

@mcp.tool(description="Restart TOR service")
async def restart_tor() -> Dict[str, Any]:
    """Restart the router's The Onion Router (TOR) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_TOR)
    return {"success": result, "action": "restart_tor", "message": "TOR service restart initiated"}

@mcp.tool(description="Restart USB idle service")
async def restart_usb_idle() -> Dict[str, Any]:
    """Restart the router's USB idle service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_USB_IDLE)
    return {"success": result, "action": "restart_usb_idle", "message": "USB idle service restart initiated"}

@mcp.tool(description="Restart WPS service")
async def restart_wps() -> Dict[str, Any]:
    """Restart the router's WPS (Wi-Fi Protected Setup) service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_WPSIE)
    return {"success": result, "action": "restart_wps", "message": "WPS service restart initiated"}

@mcp.tool(description="Restart Router Boost service")
async def restart_router_boost() -> Dict[str, Any]:
    """Restart the router's Router Boost service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_ROUTERBOOST)
    return {"success": result, "action": "restart_routerboost", "message": "Router Boost restart initiated"}

@mcp.tool(description="Restart all wired interfaces")
async def restart_net() -> Dict[str, Any]:
    """Restart all wired network interfaces on the router."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_NET)
    return {"success": result, "action": "restart_net", "message": "Network interfaces restart initiated"}

@mcp.tool(description="Restart all network interfaces (wired and wireless)")
async def restart_net_and_phy() -> Dict[str, Any]:
    """Restart all network interfaces (wired and physical) on the router."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_NET_AND_PHY)
    return {"success": result, "action": "restart_net_and_phy", "message": "All network interfaces restart initiated"}

@mcp.tool(description="Restart SNMP daemon")
async def restart_snmp() -> Dict[str, Any]:
    """Restart the router's SNMP (Simple Network Management Protocol) daemon."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_SNMPD)
    return {"success": result, "action": "restart_snmp", "message": "SNMP daemon restart initiated"}

@mcp.tool(description="Restart Line Printer Daemon")
async def restart_lpd() -> Dict[str, Any]:
    """Restart the router's Line Printer Daemon (LPD)."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_LPD)
    return {"success": result, "action": "restart_lpd", "message": "LPD restart initiated"}

@mcp.tool(description="Restart WebDAV settings")
async def restart_settings_webdav() -> Dict[str, Any]:
    """Restart the router's WebDAV settings service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_SETTINGS_WEBDAV)
    return {"success": result, "action": "restart_settings_webdav", "message": "WebDAV settings restart initiated"}

@mcp.tool(description="Restart WLC scan")
async def restart_wlc_scan() -> Dict[str, Any]:
    """Restart the router's WLC scan service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_WLCSCAN)
    return {"success": result, "action": "restart_wlcscan", "message": "WLC scan restart initiated"}

@mcp.tool(description="Restart WRS service")
async def restart_wrs() -> Dict[str, Any]:
    """Restart the router's WRS service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_WRS)
    return {"success": result, "action": "restart_wrs", "message": "WRS service restart initiated"}

@mcp.tool(description="Start WRS service")
async def start_wrs() -> Dict[str, Any]:
    """Start the router's WRS service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.START_WRS)
    return {"success": result, "action": "start_wrs", "message": "WRS service started"}

@mcp.tool(description="Force stop WRS service")
async def stop_wrs_force() -> Dict[str, Any]:
    """Force stop the router's WRS service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.STOP_WRS_FORCE)
    return {"success": result, "action": "stop_wrs_force", "message": "WRS service force stop initiated"}

@mcp.tool(description="Restart WTFast rule")
async def restart_wtfast_rule() -> Dict[str, Any]:
    """Restart the router's WTFast gaming rule service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.RESTART_WTFAST_RULE)
    return {"success": result, "action": "restart_wtfast_rule", "message": "WTFast rule restart initiated"}

@mcp.tool(description="Start Aura RGB lighting service")
async def start_aura_rgb() -> Dict[str, Any]:
    """Start the router's Aura RGB lighting service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.START_AURARGB)
    return {"success": result, "action": "start_aurargb", "message": "Aura RGB service started"}

@mcp.tool(description="Stop Aura RGB lighting service")
async def stop_aura_rgb() -> Dict[str, Any]:
    """Stop the router's Aura RGB lighting service."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.STOP_AURARGB)
    return {"success": result, "action": "stop_aurargb", "message": "Aura RGB service stopped"}

@mcp.tool(description="Start web upgrade")
async def start_webs_upgrade() -> Dict[str, Any]:
    """Start the router's firmware upgrade from the web."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.START_WEBS_UPGRADE)
    return {"success": result, "action": "start_webs_upgrade", "message": "Web upgrade started"}

@mcp.tool(description="Start web update check")
async def start_webs_update() -> Dict[str, Any]:
    """Start the router's firmware update check from the web."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.START_WEBS_UPDATE)
    return {"success": result, "action": "start_webs_update", "message": "Web update check started"}

@mcp.tool(description="Update client list")
async def update_clients() -> Dict[str, Any]:
    """Force an update of the router's client list."""
    router = await router_helper.get_router()
    result = await router.async_set_state(AsusState.SYSTEM, AsusSystem.UPDATE_CLIENTS)
    return {"success": result, "action": "update_clients", "message": "Client list update initiated"}

# LED control functions
@mcp.tool(description="Set LED state (on/off)")
async def set_led_state(state: bool) -> Dict[str, Any]:
    """Turn the router LEDs on or off."""
    router = await router_helper.get_router()
    led_state = AsusLED.ON if state else AsusLED.OFF
    result = await router.async_set_state(AsusState.LED, led_state)
    return {
        "success": result, 
        "action": "set_led", 
        "state": "on" if state else "off",
        "message": f"LEDs turned {'on' if state else 'off'}"
    }

# Aura RGB lighting control
@mcp.tool(description="Control Aura RGB lighting")
async def set_aura_lighting(
    mode: str = "static",  # static, breathing, rainbow, etc.
    color: str = "red",
    brightness: int = 100
) -> Dict[str, Any]:
    """
    Set Aura RGB lighting mode and color.
    
    Args:
        mode: Lighting mode (static, breathing, rainbow, etc.)
        color: Color name or hex value
        brightness: Brightness percentage (0-100)
    """
    router = await router_helper.get_router()
    
    # Map mode string to AsusAura enum value
    mode_map = {
        "static": AsusAura.STATIC,
        "breathing": AsusAura.BREATHING,
        "rainbow": AsusAura.RAINBOW,
        "color_cycle": AsusAura.COLOR_CYCLE,
        "wave": AsusAura.WAVE,
        "glowing": AsusAura.GLOWING,
        "off": AsusAura.OFF
    }
    
    aura_mode = mode_map.get(mode.lower(), AsusAura.STATIC)
    
    # For future extension: add color mapping logic
    # For now, use string directly as provided
    
    result = await router.async_set_state(
        AsusState.AURA, 
        aura_mode,
        color=color,
        brightness=brightness
    )
    
    return {
        "success": result,
        "action": "set_aura",
        "mode": mode,
        "color": color,
        "brightness": brightness,
        "message": f"Aura RGB set to mode: {mode}, color: {color}, brightness: {brightness}%"
    }

# WLAN (WiFi) control functions
@mcp.tool(description="Set WiFi radio state (on/off)")
async def set_wifi_radio_state(band: int, state: bool) -> Dict[str, Any]:
    """
    Turn a specific WiFi radio band on or off.
    
    Args:
        band: WiFi band index (0 for 2.4GHz, 1 for 5GHz, etc.)
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    wifi_state = AsusWLAN.ON if state else AsusWLAN.OFF
    result = await router.async_set_state(
        AsusState.WLAN, 
        wifi_state,
        api_type="wlan",
        api_id=band
    )
    return {
        "success": result,
        "action": "set_wifi_radio",
        "band": band,
        "state": "on" if state else "off",
        "message": f"WiFi radio band {band} turned {'on' if state else 'off'}"
    }

@mcp.tool(description="Set guest WiFi state (on/off)")
async def set_guest_wifi_state(band: int, state: bool) -> Dict[str, Any]:
    """
    Turn a specific guest WiFi network on or off.
    
    Args:
        band: WiFi band index (0 for 2.4GHz, 1 for 5GHz, etc.)
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    wifi_state = AsusWLAN.ON if state else AsusWLAN.OFF
    result = await router.async_set_state(
        AsusState.WLAN, 
        wifi_state,
        api_type="gwlan",
        api_id=band
    )
    return {
        "success": result,
        "action": "set_guest_wifi",
        "band": band,
        "state": "on" if state else "off",
        "message": f"Guest WiFi network on band {band} turned {'on' if state else 'off'}"
    }

# VPN control functions
@mcp.tool(description="Set OpenVPN server state (on/off)")
async def set_openvpn_server_state(state: bool) -> Dict[str, Any]:
    """
    Turn the OpenVPN server on or off.
    
    Args:
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    vpn_state = AsusOVPNServer.ON if state else AsusOVPNServer.OFF
    result = await router.async_set_state(AsusState.OPENVPN_SERVER, vpn_state)
    return {
        "success": result,
        "action": "set_openvpn_server",
        "state": "on" if state else "off",
        "message": f"OpenVPN server turned {'on' if state else 'off'}"
    }

@mcp.tool(description="Set OpenVPN client state (on/off)")
async def set_openvpn_client_state(client_id: int, state: bool) -> Dict[str, Any]:
    """
    Turn a specific OpenVPN client on or off.
    
    Args:
        client_id: Client ID (typically 1-5)
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    vpn_state = AsusOVPNClient.ON if state else AsusOVPNClient.OFF
    result = await router.async_set_state(
        AsusState.OPENVPN_CLIENT, 
        vpn_state,
        client=client_id
    )
    return {
        "success": result,
        "action": "set_openvpn_client",
        "client_id": client_id,
        "state": "on" if state else "off",
        "message": f"OpenVPN client {client_id} turned {'on' if state else 'off'}"
    }

@mcp.tool(description="Set WireGuard server state (on/off)")
async def set_wireguard_server_state(state: bool) -> Dict[str, Any]:
    """
    Turn the WireGuard server on or off.
    
    Args:
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    vpn_state = AsusWireGuardServer.ON if state else AsusWireGuardServer.OFF
    result = await router.async_set_state(AsusState.WIREGUARD_SERVER, vpn_state)
    return {
        "success": result,
        "action": "set_wireguard_server",
        "state": "on" if state else "off",
        "message": f"WireGuard server turned {'on' if state else 'off'}"
    }

@mcp.tool(description="Set WireGuard client state (on/off)")
async def set_wireguard_client_state(client_id: int, state: bool) -> Dict[str, Any]:
    """
    Turn a specific WireGuard client on or off.
    
    Args:
        client_id: Client ID (typically 1-5)
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    vpn_state = AsusWireGuardClient.ON if state else AsusWireGuardClient.OFF
    result = await router.async_set_state(
        AsusState.WIREGUARD_CLIENT, 
        vpn_state,
        client=client_id
    )
    return {
        "success": result,
        "action": "set_wireguard_client",
        "client_id": client_id,
        "state": "on" if state else "off",
        "message": f"WireGuard client {client_id} turned {'on' if state else 'off'}"
    }

@mcp.tool(description="Set VPN Fusion (VPNC) state (on/off)")
async def set_vpnc_state(vpnc_id: int, state: bool) -> Dict[str, Any]:
    """
    Turn a specific VPN Fusion (VPNC) profile on or off.
    
    Args:
        vpnc_id: VPNC profile ID (typically 1-5)
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    vpn_state = AsusVPNC.ON if state else AsusVPNC.OFF
    result = await router.async_set_state(
        AsusState.VPNC, 
        vpn_state,
        unit=vpnc_id
    )
    return {
        "success": result,
        "action": "set_vpnc",
        "vpnc_id": vpnc_id,
        "state": "on" if state else "off",
        "message": f"VPN Fusion profile {vpnc_id} turned {'on' if state else 'off'}"
    }

# Port forwarding functions
@mcp.tool(description="Set port forwarding global state (on/off)")
async def set_port_forwarding_state(state: bool) -> Dict[str, Any]:
    """
    Enable or disable port forwarding globally.
    
    Args:
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    pf_state = AsusPortForwarding.ON if state else AsusPortForwarding.OFF
    result = await router.async_set_state(AsusState.PORT_FORWARDING, pf_state)
    return {
        "success": result,
        "action": "set_port_forwarding",
        "state": "on" if state else "off",
        "message": f"Port forwarding {'enabled' if state else 'disabled'}"
    }

@mcp.tool(description="Add a port forwarding rule")
async def add_port_forwarding_rule(
    name: str,
    ip_address: str,
    protocol: str = "BOTH",
    external_port: Union[int, str] = "",
    internal_port: Union[int, str] = "",
    src_ip: str = ""
) -> Dict[str, Any]:
    """
    Add a new port forwarding rule.
    
    Args:
        name: Rule name
        ip_address: Internal IP address to forward to
        protocol: Protocol (TCP, UDP, or BOTH)
        external_port: External port or port range (e.g., "8080" or "8080:8085")
        internal_port: Internal port or port range (e.g., "80" or "80:85")
        src_ip: Source IP address restriction (optional)
    """
    router = await router_helper.get_router()
    
    # Normalize protocol
    protocol = protocol.upper()
    if protocol not in ["TCP", "UDP", "BOTH"]:
        protocol = "BOTH"
    
    # Create rule object
    rule = PortForwardingRule(
        name=name,
        ip=ip_address,
        protocol=protocol,
        port=str(external_port),
        lport=str(internal_port),
        src=src_ip
    )
    
    # Add the rule
    result = await router.async_set_port_forwarding_rules(rule)
    
    return {
        "success": result,
        "action": "add_port_forwarding_rule",
        "rule": {
            "name": name,
            "ip_address": ip_address,
            "protocol": protocol,
            "external_port": str(external_port),
            "internal_port": str(internal_port),
            "src_ip": src_ip
        },
        "message": f"Port forwarding rule '{name}' added"
    }

@mcp.tool(description="Remove a port forwarding rule")
async def remove_port_forwarding_rule(
    ip_address: str = "",
    rule_name: str = ""
) -> Dict[str, Any]:
    """
    Remove port forwarding rules based on IP address or rule name.
    
    Args:
        ip_address: IP address to remove all rules for (optional)
        rule_name: Specific rule name to remove (optional)
    """
    router = await router_helper.get_router()
    
    # Need at least one parameter
    if not ip_address and not rule_name:
        return {
            "success": False,
            "action": "remove_port_forwarding_rule",
            "message": "Either ip_address or rule_name must be provided"
        }
    
    # Get current rules
    pf_data = await router.async_get_data(AsusData.PORT_FORWARDING)
    current_rules = pf_data.get("rules", [])
    
    # Find rule to remove
    rule_to_remove = None
    for rule in current_rules:
        if (ip_address and rule.ip == ip_address) or (rule_name and rule.name == rule_name):
            rule_to_remove = rule
            break
    
    if not rule_to_remove:
        return {
            "success": False,
            "action": "remove_port_forwarding_rule",
            "message": "No matching port forwarding rule found"
        }
    
    # Remove the rule and apply
    removed_rules = await router.async_remove_port_forwarding_rules(
        ips=ip_address if ip_address else None,
        rules=rule_to_remove if rule_name else None
    )
    
    return {
        "success": len(removed_rules) > 0,
        "action": "remove_port_forwarding_rule",
        "removed": len(removed_rules),
        "message": f"Removed {len(removed_rules)} port forwarding rule(s)"
    }

@mcp.tool(description="Apply port forwarding rules")
async def apply_port_forwarding_rules() -> Dict[str, Any]:
    """Apply all pending port forwarding rules."""
    router = await router_helper.get_router()
    
    # Get current rules
    pf_data = await router.async_get_data(AsusData.PORT_FORWARDING)
    current_rules = pf_data.get("rules", [])
    
    # Apply the rules
    result = await router.async_apply_port_forwarding_rules(current_rules)
    
    return {
        "success": result,
        "action": "apply_port_forwarding_rules",
        "rules_count": len(current_rules),
        "message": f"Applied {len(current_rules)} port forwarding rules"
    }

# Parental control functions
@mcp.tool(description="Set parental control state (on/off)")
async def set_parental_control_state(state: bool) -> Dict[str, Any]:
    """
    Enable or disable parental control globally.
    
    Args:
        state: True to enable, False to disable
    """
    router = await router_helper.get_router()
    pc_state = AsusParentalControl.ON if state else AsusParentalControl.OFF
    result = await router.async_set_state(AsusState.PARENTAL_CONTROL, pc_state)
    return {
        "success": result,
        "action": "set_parental_control",
        "state": "on" if state else "off",
        "message": f"Parental control {'enabled' if state else 'disabled'}"
    }

@mcp.tool(description="Block all internet access (on/off)")
async def set_block_all_internet(state: bool) -> Dict[str, Any]:
    """
    Block internet access for all devices.
    
    Args:
        state: True to block all, False to allow
    """
    router = await router_helper.get_router()
    block_state = AsusBlockAll.ON if state else AsusBlockAll.OFF
    result = await router.async_set_state(AsusState.BLOCK_ALL, block_state)
    return {
        "success": result,
        "action": "set_block_all_internet",
        "state": "on" if state else "off",
        "message": f"Internet access for all devices {'blocked' if state else 'allowed'}"
    }

# Server main
if __name__ == "__main__":
    # Run the MCP server, defaulting to stdio transport
    mcp.run()

