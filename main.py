import os
import asyncio
import logging
import httpx
from fastapi import FastAPI, Response
from prometheus_client import make_asgi_app, Gauge, Counter, REGISTRY, generate_latest, CONTENT_TYPE_LATEST

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables
RPC_URL = os.getenv("HYPERLIQUID_RPC_URL", "https://rpc.hyperliquid.xyz/evm")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))
DISABLE_SSL_VERIFY = os.getenv("DISABLE_SSL_VERIFY", "false").lower() == "true"

# Prometheus Metrics
BLOCK_NUMBER = Gauge('hyperliquid_block_number', 'Current block number of the Hyperliquid EVM')
GAS_PRICE = Gauge('hyperliquid_gas_price', 'Current gas price in wei')
IS_SYNCING = Gauge('hyperliquid_syncing', '1 if the node is syncing, 0 otherwise')
RPC_UP = Gauge('hyperliquid_rpc_up', '1 if the RPC endpoint is reachable, 0 otherwise')
RPC_ERRORS = Counter('hyperliquid_rpc_errors_total', 'Total number of RPC errors encountered')

app = FastAPI()

# Create Prometheus ASGI app
# metrics_app = make_asgi_app()
# app.mount("/metrics", metrics_app)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

async def json_rpc_call(client: httpx.AsyncClient, method: str, params: list = []):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    try:
        response = await client.post(RPC_URL, json=payload, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            logger.error(f"RPC Error for {method}: {data['error']}")
            RPC_ERRORS.inc()
            return None
        return data.get("result")
    except Exception as e:
        logger.error(f"Exception querying {method}: {repr(e)}")
        RPC_ERRORS.inc()
        return None

async def fetch_metrics():
    """
    Background task to fetch metrics from the Hyperliquid RPC.
    """
    async with httpx.AsyncClient(verify=not DISABLE_SSL_VERIFY) as client:
        while True:
            try:
                # Check Block Number
                block_hex = await json_rpc_call(client, "eth_blockNumber")
                if block_hex:
                    BLOCK_NUMBER.set(int(block_hex, 16))
                    RPC_UP.set(1)
                else:
                    RPC_UP.set(0)

                # Check Gas Price
                gas_hex = await json_rpc_call(client, "eth_gasPrice")
                if gas_hex:
                    GAS_PRICE.set(int(gas_hex, 16))



                # Check Syncing Status
                # eth_syncing returns FALSE (boolean) if not syncing, or an object if syncing
                sync_status = await json_rpc_call(client, "eth_syncing")
                if sync_status is False:
                    IS_SYNCING.set(0)
                elif sync_status:
                    IS_SYNCING.set(1)
                    # Could extract more sync info here if needed
                
            except Exception as e:
                logger.error(f"Error in fetch loop: {e}")
                RPC_UP.set(0)

            await asyncio.sleep(POLL_INTERVAL)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting Hyperliquid Exporter. RPC URL: {RPC_URL}")
    asyncio.create_task(fetch_metrics())

@app.get("/health")
def health_check():
    return {"status": "ok"}
