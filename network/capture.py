import os
import sys
import django
from django.utils import timezone

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Setup Django
django.setup()

# Import the Packet model
from network.models import Packet

# Import scapy
from scapy.all import sniff, get_if_list, conf, IP

# Define a packet callback function for Scapy
def packet_callback(packet):
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        Packet.objects.create(
            timestamp=timezone.now(),
            source_ip=ip_layer.src,
            destination_ip=ip_layer.dst,
            protocol=ip_layer.proto,
            length=len(packet),
            info=str(packet.summary())
        )

def main():
    # List available interfaces
    interfaces = get_if_list()
    print("Available network interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")

    # Choose an interface to capture on
    iface_index = int(input("Enter the number of the interface to capture on: "))
    iface = interfaces[iface_index]

    # Set the interface to promiscuous mode
    conf.iface = iface
    conf.promisc = True

    # Start sniffing packets
    try:
        print(f"Starting packet capture on {iface}...")
        sniff(iface=iface, prn=packet_callback, filter="ip", store=0, promisc=True, timeout=60)  # Adjust timeout as needed
    except KeyboardInterrupt:
        print("Packet capture stopped.")

if __name__ == "__main__":
    main()
