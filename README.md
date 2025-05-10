# Asus Router MCP Server

This MCP server exposes **all** available functionalities of the [asusrouter](https://github.com/kennedyshead/asusrouter) Python library, allowing you to control and monitor your Asus router via Model Context Protocol (MCP) tools.

## Features

Below is a comprehensive list of all functionalities available via the AsusRouter MCP server, categorized by type with example prompts for testing.

## Table of Contents
- [Data Retrieval (Status/Info)](#data-retrieval-statusinfo)
- [Actions (State/Control)](#actions-statecontrol)
- [Port Forwarding Management](#port-forwarding-management)
- [Identity & Connection](#identity--connection)
- [WLAN Control](#wlan-control)
- [VPN Management](#vpn-management)
- [Parental Control](#parental-control)

## Data Retrieval (Status/Info)

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **aimesh**                   | Get AiMesh topology and status                                   | "Show me my AiMesh network status"                  |
| **aura**                     | Get Aura RGB lighting status                                    | "What is the current Aura RGB lighting status?"     |
| **boottime**                 | Get router boot time                                            | "When was my router last rebooted?"                 |
| **clients**                  | List all connected devices                                      | "Show me all devices connected to my network"       |
| **cpu**                      | Get CPU usage statistics                                        | "What is the current CPU usage on my router?"       |
| **devicemap**                | Get device map information                                      | "Show me the device map for my router"              |
| **dsl**                      | Get DSL line status                                             | "What is the DSL line status?"                      |
| **firmware**                 | Get firmware version and update status                          | "What firmware version is my router running?"       |
| **firmware_note**            | Get firmware release notes                                      | "Show me the latest firmware release notes"         |
| **flags**                    | Get router status flags                                         | "Show me all router status flags"                   |
| **gwlan**                    | Get guest WLAN information                                      | "Show me guest WiFi details"                        |
| **led**                      | Get LED status                                                  | "Are the router LEDs on or off?"                    |
| **network**                  | Get network statistics                                          | "Show me my network statistics"                     |
| **node_info**                | Get AiMesh node information                                     | "Show me AiMesh node details"                       |
| **openvpn**                  | Get OpenVPN status                                              | "Is OpenVPN enabled on my router?"                  |
| **openvpn_client**           | Get OpenVPN client status                                       | "Show me OpenVPN client status"                     |
| **openvpn_server**           | Get OpenVPN server status                                       | "Show me OpenVPN server status"                     |
| **parental_control**         | Get parental control status and rules                           | "Show me parental control settings"                 |
| **ping**                     | Run a network ping test                                         | "Ping google.com from my router"                    |
| **port_forwarding**          | Get port forwarding rules                                       | "List all port forwarding rules"                    |
| **ports**                    | Get Ethernet port status                                        | "Show me the status of all Ethernet ports"          |
| **ram**                      | Get RAM usage statistics                                        | "How much RAM is my router using?"                  |
| **speedtest**                | Get speedtest results                                           | "Show me the latest speedtest results"              |
| **speedtest_result**         | Get detailed speedtest result                                   | "Show me detailed speedtest results"                |
| **sysinfo**                  | Get system information (CPU, memory, load, etc.)                | "Show me system information for my router"          |
| **system**                   | Get system-level status                                         | "Show me system-level status"                       |
| **temperature**              | Get temperature sensor readings                                 | "What is the temperature of my router?"             |
| **vpnc**                     | Get VPN Fusion (VPNC) status                                    | "Show me VPN Fusion status"                         |
| **vpnc_clientlist**          | Get VPNC client list                                            | "List all VPN Fusion clients"                       |
| **wan**                      | Get WAN (Internet) connection status                            | "Show me my WAN connection status"                  |
| **wireguard**                | Get WireGuard VPN status                                        | "Show me WireGuard VPN status"                      |
| **wireguard_client**         | Get WireGuard client status                                     | "Show me WireGuard client status"                   |
| **wireguard_server**         | Get WireGuard server status                                     | "Show me WireGuard server status"                   |
| **wlan**                     | Get WLAN (WiFi) status and configuration                        | "Show me my WiFi settings"                          |

## Actions (State/Control)

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **Reboot router**            | Reboot the router                                                | "Reboot my router"                                  |
| **Restart AiMesh**           | Restart AiMesh network                                           | "Restart my AiMesh network"                         |
| **Rebuild AiMesh**           | Rebuild AiMesh topology                                         | "Rebuild my AiMesh network"                         |
| **Restart Aura RGB**         | Restart Aura RGB lighting                                       | "Restart Aura RGB lighting"                         |
| **Check firmware update**    | Check for firmware updates                                      | "Check for firmware updates"                        |
| **Upgrade firmware**         | Upgrade router firmware                                         | "Upgrade my router firmware"                        |
| **Restart firewall**         | Restart the firewall                                            | "Restart the firewall"                              |
| **Restart web server**       | Restart the router's web server                                 | "Restart the router web server"                     |
| **Restart Samba**            | Restart Samba file sharing                                      | "Restart Samba file sharing"                        |
| **Restart WAN**              | Restart WAN (Internet) connection                               | "Restart my WAN connection"                         |
| **Restart wireless**         | Restart all wireless interfaces                                 | "Restart all wireless interfaces"                   |
| **Restart OpenVPN**          | Restart OpenVPN daemon                                          | "Restart OpenVPN service"                           |
| **Restart WireGuard**        | Restart all WireGuard server interfaces                         | "Restart WireGuard server interfaces"               |
| **Restart UPNP**             | Restart Universal Plug and Play                                 | "Restart UPNP service"                              |
| **Restart DNS**              | Restart DNS service                                             | "Restart DNS service"                               |
| **Restart time service**     | Restart time synchronization                                    | "Restart time synchronization service"              |
| **Restart FTP**              | Restart FTP server                                              | "Restart FTP server"                                |
| **Restart LEDs**             | Restart router LEDs                                             | "Restart router LEDs"                               |
| **Restart cloud sync**       | Restart AiCloud 2.0 sync                                        | "Restart AiCloud sync"                              |
| **Restart captive portal**   | Restart captive portal                                          | "Restart captive portal"                            |
| **Restart DDNS**             | Restart dynamic DNS                                             | "Restart dynamic DNS"                               |
| **Restart disk monitor**     | Restart disk monitor                                            | "Restart disk monitor"                              |
| **Restart QOS**              | Restart Quality of Service                                      | "Restart QoS service"                               |
| **Restart VPNC**             | Restart VPN Fusion                                              | "Restart VPN Fusion"                                |
| **Restart VPND**             | Restart legacy VPN daemon                                       | "Restart legacy VPN service"                        |
| **Restart webdav**           | Restart WebDAV service                                          | "Restart WebDAV service"                            |
| **Restart subnet**           | Restart subnet                                                  | "Restart subnet"                                    |
| **Restart time machine**     | Restart Time Machine backup                                     | "Restart Time Machine backup"                       |
| **Restart TOR**              | Restart The Onion Router                                        | "Restart TOR service"                               |
| **Restart USB idle**         | Restart USB idle service                                        | "Restart USB idle service"                          |
| **Restart WPS**              | Restart WPS service                                             | "Restart WPS service"                               |
| **Restart router boost**     | Restart router boost                                            | "Restart router boost"                              |
| **Restart net**              | Restart all wired interfaces                                    | "Restart all wired interfaces"                      |
| **Restart net and phy**      | Restart all network interfaces                                  | "Restart all network interfaces"                    |
| **Restart SNMPD**            | Restart SNMP daemon                                             | "Restart SNMP daemon"                               |
| **Restart LPD**              | Restart Line Printer Daemon                                     | "Restart LPD service"                               |
| **Restart settings webdav**  | Restart settings WebDAV                                         | "Restart settings WebDAV"                           |
| **Restart WLC scan**         | Restart WLC scan                                                | "Restart WLC scan"                                  |
| **Restart WRS**              | Restart WRS                                                     | "Restart WRS"                                       |
| **Restart Wtfast rule**      | Restart Wtfast rule                                             | "Restart Wtfast rule"                               |
| **Reset LED**                | Reset router LED                                                | "Reset router LED"                                  |
| **Start Aura RGB**           | Start Aura RGB lighting                                         | "Start Aura RGB lighting"                           |
| **Start disk format**        | Start disk format                                               | "Format attached disk"                              |
| **Start disk scan**          | Start disk scan                                                 | "Scan attached disk"                                |
| **Start web upgrade**        | Start firmware upgrade from web                                 | "Start firmware upgrade from web"                   |
| **Start web update**         | Start firmware update from web                                  | "Start firmware update from web"                    |
| **Stop Aura RGB**            | Stop Aura RGB lighting                                          | "Stop Aura RGB lighting"                            |
| **Stop OpenVPN**             | Stop OpenVPN server                                             | "Stop OpenVPN server"                               |
| **Stop VPNC**                | Stop VPN Fusion                                                 | "Stop VPN Fusion"                                   |
| **Stop VPND**                | Stop legacy VPN daemon                                          | "Stop legacy VPN service"                           |
| **Stop WRS force**           | Force stop WRS                                                  | "Force stop WRS"                                    |
| **Update clients**           | Update client list                                              | "Update client list"                                |

## Port Forwarding Management

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **Add port forwarding rule** | Add a new port forwarding rule                                   | "Add a port forwarding rule for port 8080 to 192.168.1.100" |
| **Remove port forwarding rule** | Remove a port forwarding rule                                 | "Remove the port forwarding rule for port 8080"     |
| **Apply port forwarding rules** | Apply all port forwarding rules                               | "Apply all port forwarding rules"                   |

## Identity & Connection

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **Get router identity**      | Get router model, serial, firmware, etc.                         | "Show me my router's identity and model"            |
| **Connect to router**        | Establish connection to the router                               | "Connect to my router"                              |
| **Disconnect from router**   | Disconnect from the router                                       | "Disconnect from my router"                         |

## WLAN Control

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **Enable/disable WiFi**      | Turn WiFi on or off                                              | "Turn off my router's WiFi"                         |
| **Enable/disable guest WiFi**| Control guest WiFi networks                                     | "Enable guest WiFi network"                         |
| **Change WiFi settings**     | Update WiFi configuration                                       | "Change my WiFi channel to 6"                       |
| **Get WiFi clients**         | List clients connected via WiFi                                 | "Show me all devices connected to WiFi"             |

## VPN Management

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **Enable/disable OpenVPN server** | Control OpenVPN server                                      | "Enable OpenVPN server"                             |
| **Enable/disable WireGuard server** | Control WireGuard server                                  | "Turn on WireGuard server"                          |
| **Get OpenVPN client status**| Check status of OpenVPN clients                                 | "Show status of all OpenVPN clients"                |
| **Get WireGuard client status**| Check status of WireGuard clients                            | "Show status of all WireGuard clients"              |
| **Enable/disable VPN Fusion**| Control VPN Fusion (VPNC)                                       | "Turn on VPN Fusion"                                |

## Parental Control

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **Enable/disable parental control** | Turn parental control on or off                          | "Enable parental control on my router"              |
| **Add parental control rule**| Add a new parental control rule                                 | "Add parental control rule for device MAC 00:11:22:33:44:55" |
| **Remove parental control rule** | Remove a parental control rule                             | "Remove parental control rule for device MAC 00:11:22:33:44:55" |
| **Block all devices**        | Block internet access for all devices                           | "Block internet access for all devices temporarily"  |

## LED Control

| Functionality                | Description                                                      | Example Prompt                                      |
|------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| **Enable/disable LEDs**      | Turn router LEDs on or off                                      | "Turn off router LEDs"                              |
| **Control Aura RGB lighting**| Manage Aura RGB lighting settings                               | "Change Aura RGB lighting to red"                   |

## How to Use

For each functionality, you can use the example prompt as a template to interact with the MCP server. The server will expose all of these features as MCP tools or resources, allowing you to automate, monitor, and control your Asus router programmatically.

> **Note:** Some functions may require specific router models/firmware and may not be available on all devices.