import json
import heapq
import socket
import sys

def get_hostname(ip: str):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return " --- "


with open(sys.argv[1]) as f:
    packets = json.load(f)

d = dict()

for packet in packets:
    try:
        ip = packet['_source']['layers']['ip']['ip.dst']
        if ip.startswith("192.168"):
            continue
        d[ip] = d.get(ip, 0) + 1

    except Exception:
        pass

# for ip in d:
#     print(f"{ip} -> {d[ip]}")

top_3 = heapq.nlargest(3, d, key=d.get)

for ip in top_3:
    print("{} -> {}".format(ip, get_hostname(ip)))

