# ASUS Router MCP Server

## Thesis Project Overview

This repository contains an MCP (Message Control Protocol) server implementation for ASUS routers, providing a comprehensive programmatic interface to monitor and control router functions. The server exposes a wide range of router capabilities as easy-to-use tools that can be integrated with chatbots, smart home systems, or custom applications.

## Features

- **Complete Router Management** - Control and monitor virtually all aspects of your ASUS router
- **Rich Data Retrieval** - Get detailed information about connected devices, network status, and system health
- **Configuration Tools** - Modify router settings including WiFi, LED controls, and more
- **Diagnostic Capabilities** - Run speed tests, check temperatures, and monitor resource usage
- **Secure Access** - Proper authentication and security practices for router control

## Requirements

- Python 3.8+
- `aiohttp` library
- `asusrouter` library
- ASUS router with accessible web interface

## Installation

1. Clone this repository:
   ```
   git clone [repository-url]
   ```

2. Install dependencies:
   ```
   pip install mcp-server asusrouter aiohttp
   ```

3. Configure your router connection details in `server.py`:
   ```python
   ROUTER_CONFIG = {
       "hostname": "your-router-ip",
       "username": "your-username",
       "password": "your-password",
       "use_ssl": False  # Set to True if your router uses HTTPS
   }
   ```

4. Run the server:
   ```
   python server.py
   ```

## Available Tools

The server provides tools in several categories:

### Network Information

- `get_connected_devices` - List all devices connected to the router
- `get_wlan_status` - Get WiFi configuration details
- `get_network_status` - Get traffic statistics for all interfaces
- `get_wan_status` - Check WAN connection details
- `get_port_forwarding` - View port forwarding rules
- `get_guest_wifi_status` - Check guest network configuration
- `get_ports_status` - Monitor physical network port status
- `get_devicemap` - Get comprehensive device mapping

### System Information

- `get_system_info` - Get router hardware and software details
- `get_cpu_ram_usage` - Monitor resource utilization
- `get_temperature` - Check router temperature
- `get_boottime` - Get uptime information
- `get_firmware_info` - Check firmware version and updates
- `get_aimesh_info` - Get mesh network topology information
- `get_parental_control` - Check content filtering settings
- `get_led_status` - Get LED indicator status
- `get_vpn_config` - Monitor VPN configurations
- `get_dsl_status` - Check DSL connection status (if applicable)

### Configuration Controls

- `set_wifi_settings` - Modify wireless network settings
- `set_led_state` - Control router LED indicators
- `set_aura_lighting` - Control AURA RGB lighting effects
- `reboot_router` - Restart the router

### Diagnostics

- `run_speedtest` - Test internet connection speed

## Usage Examples

### Retrieving Connected Devices

```python
from mcp.client import MCPClient

client = MCPClient("your-mcp-server-address")
devices = await client.call_tool("get_connected_devices")
print(f"Connected devices: {devices}")
```

### Changing WiFi Settings

```python
# Set 5GHz WiFi network name and password
result = await client.call_tool(
    "set_wifi_settings", 
    band="5ghz", 
    ssid="MyHomeNetwork_5G", 
    password="SecurePassword123"
)
print(result["message"])
```

### Running a Speed Test

```python
# Initiate a speed test from the router
result = await client.call_tool("run_speedtest")
print(f"Download speed: {result['speedtest_result']['download']} Mbps")
print(f"Upload speed: {result['speedtest_result']['upload']} Mbps")
print(f"Ping: {result['speedtest_result']['ping']} ms")
```

## Advanced Features

- **AiMesh Support** - Monitor and manage mesh networks
- **AURA RGB Lighting Control** - Customize lighting effects on supported routers
- **Guest WiFi Management** - Configure visitor access
- **VPN Configuration** - Monitor OpenVPN and WireGuard setups

## Security Considerations

This server provides powerful control over your router. Always:
- Run on a secured network
- Use strong authentication credentials
- Consider implementing additional authentication for the MCP server
- Review logs regularly for unauthorized access attempts

## License

[Your License Information]

## Author

[Your Name]

## Acknowledgments

- ASUS Router community
- AsusRouter Python library developers
- [Other acknowledgments] 