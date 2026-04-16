from icmplib import ping
import pandas as pd


domains = [
    "google.com",
    "yandex.ru",
    "github.com",
    "stackoverflow.com",
    "wikipedia.org",
    "bing.com",
    "amazon.com",
    "microsoft.com",
    "reddit.com",
    "openai.com"
]

data = pd.DataFrame(columns=["Domain", "Min RTT", "Max RTT", "Avg RTT", "Packets Sent", "Packets Received", "Packet Loss"])

for domain in domains:
    host = ping(domain, count=5)
    data = pd.concat([data, pd.DataFrame([{
        "Domain": domain,
        "Min RTT": host.min_rtt,
        "Max RTT": host.max_rtt,
        "Avg RTT": host.avg_rtt,
        "Packets Sent": host.packets_sent,
        "Packets Received": host.packets_received,
        "Packet Loss": host.packet_loss
    }])], ignore_index=True)

data.to_csv("domain_inf.csv", sep = " ", index=False)