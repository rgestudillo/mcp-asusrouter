from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from asusrouter import AsusRouter, AsusData
import uvicorn
from typing import Dict, Any

app = FastAPI(title="ASUS Router API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router configuration
ROUTER_CONFIG = {
    "hostname": "192.168.72.1",
    "username": "admin",
    "password": "Regina143$#",
    "use_ssl": False
}

@app.get("/")
async def root():
    return {"message": "ASUS Router API is running"}

@app.get("/router-data/{data_type}")
async def get_router_data(data_type: str) -> Dict[str, Any]:
    try:
        # Validate data type
        try:
            asus_data = AsusData[data_type.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid data type: {data_type}")

        # Create an aiohttp session
        async with aiohttp.ClientSession() as session:
            router = AsusRouter(
                hostname=ROUTER_CONFIG["hostname"],
                username=ROUTER_CONFIG["username"],
                password=ROUTER_CONFIG["password"],
                use_ssl=ROUTER_CONFIG["use_ssl"],
                session=session
            )

            try:
                # Connect to the router
                await router.async_connect()
                
                # Fetch the requested data
                data = await router.async_get_data(asus_data)
                
                if data is None:
                    return {"message": f"No data available for {data_type}"}
                
                return {"data": data}

            finally:
                # Always disconnect from the router
                await router.async_disconnect()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/available-data-types")
async def get_available_data_types():
    """Return a list of all available data types and their descriptions"""
    data_types = {
        "AIMESH": "AiMesh Configuration",
        "AURA": "Aura RGB Status",
        "BOOTTIME": "Boot Time",
        "CLIENTS": "Connected Devices",
        "CPU": "CPU Usage",
        "DEVICEMAP": "Device Map",
        "DSL": "DSL Status",
        "FIRMWARE": "Firmware Info",
        "FIRMWARE_NOTE": "Firmware Update Notes",
        "FLAGS": "System Flags",
        "GWLAN": "Guest WLAN Settings",
        "LED": "LED Control Status",
        "NETWORK": "Network Stats",
        "NODE_INFO": "Node Information (AiMesh)",
        "OPENVPN": "OpenVPN General Status",
        "OPENVPN_CLIENT": "OpenVPN Client Status",
        "OPENVPN_SERVER": "OpenVPN Server Status",
        "PARENTAL_CONTROL": "Parental Control Settings",
        "PING": "Ping Test Results",
        "PORT_FORWARDING": "Port Forwarding Rules",
        "PORTS": "Ethernet Ports",
        "RAM": "RAM Usage",
        "SPEEDTEST": "Speedtest Results",
        "SPEEDTEST_RESULT": "Speedtest Result Details",
        "SYSINFO": "System Information",
        "SYSTEM": "System Status",
        "TEMPERATURE": "Temperature Readings",
        "VPNC": "VPN Client Status (PPTP/L2TP)",
        "VPNC_CLIENTLIST": "VPN Client List",
        "WAN": "WAN Status",
        "WIREGUARD": "WireGuard General Status",
        "WIREGUARD_CLIENT": "WireGuard Client Status",
        "WIREGUARD_SERVER": "WireGuard Server Status",
        "WLAN": "WLAN Settings"
    }
    return {"data_types": data_types}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True) 