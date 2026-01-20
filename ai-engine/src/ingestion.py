import time
import requests
import pandas as pd
from datetime import datetime

PROMETHEUS_URL = "http://localhost:9090"

# Cluster-wide CPU usage rate
QUERY = 'sum(rate(container_cpu_usage_seconds_total[1m]))'

window = []
WINDOW_SIZE = 20   # rolling window (~10 minutes if 30s interval)


def query_prometheus():
    url = f"{PROMETHEUS_URL}/api/v1/query"
    response = requests.get(url, params={"query": QUERY})
    data = response.json()

    if data["status"] != "success":
        return None

    result = data["data"]["result"]
    if not result:
        return None

    return float(result[0]["value"][1])


def detect_anomaly(value):
    window.append(value)

    if len(window) < WINDOW_SIZE:
        return None

    series = pd.Series(window[-WINDOW_SIZE:])
    mean = series.mean()
    std = series.std()

    # 3-sigma anomaly rule
    if std > 0 and value > mean + 3 * std:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metric": "cluster_cpu_rate",
            "value": value,
            "mean": mean,
            "std": std
        }

    return None


def main():
    print("🚀 AI Metric Ingestion Service started")

    while True:
        value = query_prometheus()

        if value is not None:
            anomaly = detect_anomaly(value)
            print(f"[{datetime.utcnow().isoformat()}] CPU rate = {value:.5f}")

            if anomaly:
                print("🚨 INCIDENT DETECTED:", anomaly)

        time.sleep(30)


if __name__ == "__main__":
    main()
