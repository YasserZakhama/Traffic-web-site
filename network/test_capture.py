from scapy.all import sniff

def packet_callback(packet):
    print(f"Captured packet: {packet.summary()}")

print("Starting packet capture...")
sniff(prn=packet_callback, filter="ip", store=0)
