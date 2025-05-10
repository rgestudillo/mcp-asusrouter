# ASUS Router MCP

This package provides a comprehensive suite of tools for interacting with ASUS routers via the FastMCP framework. It leverages the `asusrouter` Python library to enable remote monitoring and management of your ASUS Router.

## Installation

```bash
pip install mcp
pip install aiohttp
pip install asusrouter
```

## Configuration

By default, the tools are configured to connect to a router at `192.168.72.1` with the username `admin`. You can modify the `ROUTER_CONFIG` dictionary in the script to match your router's details:

```python
ROUTER_CONFIG = {
    "hostname": "192.168.72.1",
    "username": "admin",
    "password": "your_password_here",
    "use_ssl": False
}
```

## Available Tools

Below are all available tools with descriptions and numbered example prompts.

### Device Information

1. **get_connected_devices**
   Retrieves information about all devices connected to your router.

   Example prompt:
   ```
   Show me all devices connected to my network right now
   ```

2. **get_aimesh_info**
   Gets information about your AiMesh setup and node status.

   Example prompt:
   ```
   What's the status of my AiMesh network? Are all nodes connected?
   ```

3. **get_boottime**
   Retrieves the router's boot time and calculates uptime.

   Example prompt:
   ```
   How long has my router been running since the last reboot?
   ```

### Network Status

4. **get_network_status**
   Retrieves traffic statistics for all network interfaces.

   Example prompt:
   ```
   What's my current network utilization across all interfaces?
   ```

5. **get_wan_status**
   Gets detailed WAN (internet) connection status and configuration.

   Example prompt:
   ```
   Show me my internet connection details and public IP address
   ```

6. **get_wlan_status**
   Retrieves detailed wireless network configuration.

   Example prompt:
   ```
   What are my current WiFi settings for all bands?
   ```

7. **get_guest_wifi_status**
   Gets guest WiFi network status and configuration.

   Example prompt:
   ```
   Are any guest networks currently enabled on my router?
   ```

8. **get_ports_status**
   Retrieves the status of physical network ports.

   Example prompt:
   ```
   Which physical ports on my router are currently active and what are their speeds?
   ```

9. **get_dsl_status**
   Retrieves DSL connection status and line information for DSL routers.

   Example prompt:
   ```
   What's my DSL connection quality and sync speed?
   ```

10. **run_speedtest**
    Initiates a speed test directly from the router.

    Example prompt:
    ```
    Run a speed test from my router to check my connection speed
    ```

11. **ping_host_from_router**
    Pings a specified host from the router itself.

    Example prompt:
    ```
    Ping google.com from my router to check connectivity
    ```

### System Performance

12. **get_system_info**
    Retrieves comprehensive system information.

    Example prompt:
    ```
    Give me a complete system overview of my router
    ```

13. **get_cpu_ram_usage**
    Gets CPU and RAM utilization statistics.

    Example prompt:
    ```
    What's the current CPU and RAM usage on my router?
    ```

14. **get_temperature**
    Retrieves temperature readings from various sensors.

    Example prompt:
    ```
    Is my router running hot? Show me all temperature readings
    ```

15. **get_firmware_info**
    Gets firmware version and update availability information.

    Example prompt:
    ```
    Check if there's a firmware update available for my router
    ```

16. **check_firmware_updates**
    Triggers a check for new firmware updates.

    Example prompt:
    ```
    Force check for new firmware updates now
    ```

17. **start_firmware_upgrade**
    Initiates a firmware upgrade if an update is available.

    Example prompt:
    ```
    Upgrade my router to the latest firmware
    ```

### Network Security & Management

18. **get_parental_control**
    Retrieves parental control configuration and rule settings.

    Example prompt:
    ```
    Show me my current parental control settings and active rules
    ```

19. **set_parental_control_global_state**
    Enables or disables the Parental Controls feature globally.

    Example prompt:
    ```
    Enable parental controls on my router
    ```

20. **set_parental_control_block_all**
    Enables or disables the 'Block All Internet Access' feature.

    Example prompt:
    ```
    Block all internet access for all devices right now
    ```

21. **get_port_forwarding**
    Gets port forwarding rules and configuration.

    Example prompt:
    ```
    List all my configured port forwarding rules
    ```

22. **set_port_forwarding_global_state**
    Enables or disables Port Forwarding globally.

    Example prompt:
    ```
    Disable all port forwarding rules temporarily
    ```

### VPN Management

23. **get_vpn_config**
    Retrieves VPN client and server configuration status.

    Example prompt:
    ```
    Show me the status of all my VPN configurations
    ```

24. **get_vpn_fusion_status**
    Gets VPN Fusion (VPNC) status and configurations.

    Example prompt:
    ```
    What's the current status of my VPN Fusion profiles?
    ```

25. **control_openvpn_client**
    Enables or disables a specific OpenVPN client profile.

    Example prompt:
    ```
    Connect to my OpenVPN client profile #2
    ```

26. **control_openvpn_server**
    Enables or disables a specific OpenVPN server.

    Example prompt:
    ```
    Turn off my OpenVPN server
    ```

27. **control_wireguard_client**
    Enables or disables a specific WireGuard client profile.

    Example prompt:
    ```
    Connect to my WireGuard VPN #1
    ```

28. **control_wireguard_server**
    Enables or disables a specific WireGuard server.

    Example prompt:
    ```
    Enable my WireGuard server to allow remote connections
    ```

29. **control_vpn_fusion_client**
    Enables or disables a VPN Fusion client profile.

    Example prompt:
    ```
    Disconnect from VPN Fusion profile unit 1
    ```

### WiFi Management

30. **set_wifi_settings**
    Configures wireless network settings.

    Example prompt:
    ```
    Change my 5GHz WiFi password to "NewSecurePassword2023!"
    ```

31. **set_wifi_radio_state**
    Enables or disables the radio for a specific WiFi band.

    Example prompt:
    ```
    Turn off my 2.4GHz WiFi radio but leave 5GHz on
    ```

### System Maintenance

32. **reboot_router**
    Initiates a router reboot.

    Example prompt:
    ```
    Reboot my router now
    ```

33. **rebuild_aimesh_network**
    Triggers a rebuild of the AiMesh network.

    Example prompt:
    ```
    My mesh network seems unstable, rebuild the AiMesh network
    ```

34. **restart_dns_service**
    Restarts the DNS service on the router.

    Example prompt:
    ```
    I'm having DNS issues, restart the DNS service
    ```

35. **restart_httpd_service**
    Restarts the router's web server.

    Example prompt:
    ```
    The router admin page is sluggish, restart the HTTPD service
    ```

### LED & Lighting Control

36. **get_led_status**
    Gets router LED status information.

    Example prompt:
    ```
    Are my router LED lights currently on or off?
    ```

37. **set_led_state**
    Turns router LEDs on or off.

    Example prompt:
    ```
    Turn off all the LED lights on my router for the night
    ```

38. **set_aura_lighting**
    Controls ASUS AURA RGB lighting effects.

    Example prompt:
    ```
    Set my router RGB lighting to static red at 80% brightness
    ```

### Advanced Tools

39. **get_devicemap**
    Gets comprehensive device map information (raw data).

    Example prompt:
    ```
    Show me the detailed devicemap data from my router
    ```

40. **get_router_flags**
    Gets internal router flags and states.

    Example prompt:
    ```
    Show me all internal router flags for debugging
    ```

41. **get_vpn_fusion_client_list_raw**
    Gets the raw VPN Fusion client list string.

    Example prompt:
    ```
    Show me the raw VPN Fusion client list configuration string
    ```

## Example Usage in Code

```python
from mcp.server.fastmcp import FastMCP
import asyncio

# Initialize the MCP server
mcp = FastMCP("Asus Router MCP Server", dependencies=["aiohttp", "asusrouter"])

# Define the tools as in the main script

# Run the server
if __name__ == "__main__":
    # Test a specific tool
    async def test_connected_devices():
        result = await get_connected_devices()
        print(result)
    
    # Run the test
    asyncio.run(test_connected_devices())
    
    # Or run the full MCP server
    # mcp.run()
```

## Security Considerations

- This script stores your router credentials in plain text. Consider implementing a more secure credential management approach for production.
- All tools execute commands on your router. Be cautious when using tools that modify settings or reboot the device.
- Some operations may cause temporary network disruptions or service interruptions.

## Contributions

Feel free to extend this set of tools with additional functionality. The `asusrouter` library offers many more capabilities that could be exposed through additional MCP tools.

## License

This script is provided as-is under the MIT license.