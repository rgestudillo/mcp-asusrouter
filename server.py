from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from asusrouter import AsusRouter, AsusData
import uvicorn
from typing import Dict, Any, Tuple

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

@app.get("/")
async def root():
    return {"message": "ASUS Router API is running"}

@app.get("/devices")
async def get_connected_devices() -> Dict[str, Any]:
    try:
        router, session = await create_router_connection()
        try:
            # Fetch connected devices data
            data = await router.async_get_data(AsusData.CLIENTS)
            
            if data is None:
                return {"message": "No connected devices data available"}
            
            return {"devices": data}

        finally:
            # Always disconnect from the router and close the session
            await router.async_disconnect()
            await session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/wlan")
async def get_wlan_status() -> Dict[str, Any]:
    try:
        router, session = await create_router_connection()
        try:
            # Fetch WLAN data
            data = await router.async_get_data(AsusData.WLAN)
            
            if data is None:
                return {"message": "No WLAN data available"}
            
            return {"wlan": data}

        finally:
            await router.async_disconnect()
            await session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/network")
async def get_network_status() -> Dict[str, Any]:
    try:
        router, session = await create_router_connection()
        try:
            # Fetch network data
            data = await router.async_get_data(AsusData.NETWORK)
            
            if data is None:
                return {"message": "No network data available"}
            
            return {"network": data}

        finally:
            await router.async_disconnect()
            await session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/parental-control")
async def get_parental_control() -> Dict[str, Any]:
    try:
        router, session = await create_router_connection()
        try:
            # Fetch parental control data
            data = await router.async_get_data(AsusData.PARENTAL_CONTROL)
            
            if data is None:
                return {"message": "No parental control data available"}
            
            return {"parental_control": data}

        finally:
            await router.async_disconnect()
            await session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reboot")
async def reboot_router() -> Dict[str, Any]:
    """
    Reboot the ASUS router.
    Returns a success message if the reboot command is sent successfully.
    Note: The router will be offline for 1-2 minutes during the reboot.
    """
    try:
        router, session = await create_router_connection()
        try:
            # Send the reboot command
            result = await router.async_run_service("reboot", apply=True)
            
            return {
                "message": "Reboot command sent successfully. The router will restart now.",
                "note": "It may take 1-2 minutes for the router to come back online."
            }

        finally:
            await router.async_disconnect()
            await session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rebooting router: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)