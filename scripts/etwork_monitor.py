class NetworkMonitor:
    def inspect(self, packet_data: dict) -> dict:
        return {
            "status": "monitored",
            "packet": packet_data,
        }