# ASUS Router MCP Server

## Model Context Protocol Implementation for ASUS Routers

This repository contains a Model Context Protocol (MCP) server implementation for ASUS routers, enabling AI assistants like Claude to directly interact with and control router functions. By following Anthropic's open MCP standard, this server bridges the gap between large language models and your home network infrastructure.

## What is Model Context Protocol (MCP)?

MCP is an open standard introduced by Anthropic that enables secure, two-way connections between AI systems and data sources. It allows models like Claude to access real-time information and perform actions on external systems without requiring custom integrations for each use case.

This implementation serves as a specialized connector that exposes ASUS router capabilities through standardized tools, allowing AI assistants to:
- Retrieve real-time network information
- Monitor connected devices and system health
- Configure router settings
- Perform diagnostic tests

## Features

- **MCP-compatible Tools** - Exposes router functions as standardized tools for AI assistants
- **Complete Router Management** - Control and monitor virtually all aspects of your ASUS router
- **Rich Data Retrieval** - Get detailed information about connected devices, network status, and system health
- **Configuration Controls** - Modify router settings including WiFi, LED controls, and more
- **Diagnostic Capabilities** - Run speed tests, check temperatures, and monitor resource usage

## Requirements

- Python 3.8+
- `aiohttp` library
- `asusrouter` library
- `mcp-server` library
- ASUS router with accessible web interface
- Claude Desktop app or other MCP client

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

4. Run the MCP server:
   ```
   python server.py
   ```

5. Connect to the server from the Claude Desktop app:
   - Open Claude Desktop
   - Go to Settings > Model Context Protocol
   - Add a new connection to your locally running MCP server

## Available MCP Tools

The server provides the following tools to AI assistants:

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

## Usage with Claude

Once connected to Claude or another MCP-compatible AI assistant, you can interact with your router through natural language:

- "Show me all devices currently connected to my network"
- "What's my current WiFi configuration?"
- "Change my 5GHz WiFi password to something more secure"
- "Run a speed test and tell me the results"
- "Is my router running hot? Check the temperature"
- "Turn off the LED lights on my router for the night"

The AI assistant will use the appropriate MCP tools to retrieve information or perform actions based on your requests.

## Integration Examples

### For Developers Using the MCP Client SDK

```python
from mcp.client import MCPClient

async def get_router_info():
    # Connect to your MCP server
    client = MCPClient("your-mcp-server-address")
    
    # Get connected devices
    devices = await client.call_tool("get_connected_devices")
    print(f"Connected devices: {devices}")
    
    # Check router temperature
    temp = await client.call_tool("get_temperature")
    print(f"Router temperature: {temp}")
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

## Security Considerations

This MCP server provides powerful control over your router. Always:
- Run on a secured network
- Use strong authentication credentials
- Consider implementing additional authentication for the MCP server
- Review logs regularly for unauthorized access attempts
- Configure proper access controls in Claude Desktop for MCP connections

## Author

Refino Kashi Kyle G. Estudillo

## Acknowledgments

- Anthropic for the Model Context Protocol specification
- ASUS Router community
- AsusRouter Python library developers 