import time

import pandas as pd
import requests
import seaborn as sns
from matplotlib import pyplot as plt
from redis import Redis


URL = "http://localhost:8000/events/1"
KEY = "event:summary:1"
RUNS = 10

redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def time_request():
    start = time.perf_counter()

    response = requests.get(URL)
    response.raise_for_status()

    return (time.perf_counter() - start) * 1000


database_times = []

for _ in range(RUNS):
    redis_client.delete(KEY)
    database_times.append(time_request())

redis_client.delete(KEY)
requests.get(URL).raise_for_status()

redis_times = [
    time_request()
    for _ in range(RUNS)
]

results = pd.DataFrame({
    "Database": database_times,
    "Redis": redis_times
})

summary = results.agg(["min", "max", "mean", "median"]).T.round(2)
summary.index.name = "Metric"
summary.columns = ["Minimum (ms)", "Maximum (ms)", "Average (ms)", "Median (ms)"]

print("\nPerformance Summary\n")
print(summary)

results.to_csv("cache_benchmark_results.csv", index=False)
summary.to_csv("cache_benchmark_summary.csv")

sns.set_theme(style="whitegrid")

ax = sns.boxplot(
    data=results,
    palette=["#E15759", "#4E79A7"]
)

ax.set_title("Event Retrieval Performance: Database vs Redis Cache")
ax.set_xlabel("Retrieval Path")
ax.set_ylabel("Response Time (ms)")

plt.tight_layout()
plt.savefig("cache_performance_comparison.png", dpi=200)