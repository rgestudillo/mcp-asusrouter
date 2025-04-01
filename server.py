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

@app.get("/devices")
async def get_connected_devices() -> Dict[str, Any]:
    try:
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
                
                # Fetch connected devices data
                data = await router.async_get_data(AsusData.CLIENTS)
                
                if data is None:
                    return {"message": "No connected devices data available"}
                
                return {"devices": data}

            finally:
                # Always disconnect from the router
                await router.async_disconnect()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True) 