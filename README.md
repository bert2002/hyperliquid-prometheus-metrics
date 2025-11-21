# Hyperliquid Prometheus Exporter

A simple Prometheus exporter for Hyperliquid EVM node metrics. It queries a standard Ethereum JSON-RPC endpoint and exposes metrics at `/metrics`.

## Metrics

- `hyperliquid_block_number`: Current block number.
- `hyperliquid_gas_price`: Current gas price in wei.
- `hyperliquid_syncing`: 1 if syncing, 0 otherwise.
- `hyperliquid_rpc_up`: 1 if the RPC endpoint is reachable, 0 otherwise.
- `hyperliquid_rpc_errors_total`: Total count of RPC errors.

## Configuration

The application is configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `HYPERLIQUID_RPC_URL` | The JSON-RPC endpoint URL | `https://rpc.hyperliquid.xyz/evm` |
| `POLL_INTERVAL` | Polling interval in seconds | `5` |
| `DISABLE_SSL_VERIFY` | Set to `true` to disable SSL certificate verification | `false` |

## Running with Docker

1. Build the image:
   ```bash
   docker build -t hyperliquid-prometheus-metrics .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 -e HYPERLIQUID_RPC_URL=https://rpc.hyperliquid.xyz/evm hyperliquid-prometheus-metrics
   ```

3. Access metrics at `http://localhost:8000/metrics`.

## Metrics

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 53807.0
python_gc_objects_collected_total{generation="1"} 5531.0
python_gc_objects_collected_total{generation="2"} 897.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 182.0
python_gc_collections_total{generation="1"} 16.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="12",patchlevel="12",version="3.12.12"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 2.1551104e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 4.2692608e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.76371316768e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 14.64
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 11.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP hyperliquid_block_number Current block number of the Hyperliquid EVM
# TYPE hyperliquid_block_number gauge
hyperliquid_block_number 1.9785884e+07
# HELP hyperliquid_gas_price Current gas price in wei
# TYPE hyperliquid_gas_price gauge
hyperliquid_gas_price 2.270447005e+09
# HELP hyperliquid_syncing 1 if the node is syncing, 0 otherwise
# TYPE hyperliquid_syncing gauge
hyperliquid_syncing 0.0
# HELP hyperliquid_rpc_up 1 if the RPC endpoint is reachable, 0 otherwise
# TYPE hyperliquid_rpc_up gauge
hyperliquid_rpc_up 1.0
# HELP hyperliquid_rpc_errors_total Total number of RPC errors encountered
# TYPE hyperliquid_rpc_errors_total counter
hyperliquid_rpc_errors_total 45.0
# HELP hyperliquid_rpc_errors_created Total number of RPC errors encountered
# TYPE hyperliquid_rpc_errors_created gauge
hyperliquid_rpc_errors_created 1.7637131695591745e+09
```
