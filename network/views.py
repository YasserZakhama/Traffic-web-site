# network/views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .models import Packet
from datetime import datetime
import scapy.all as scapy
from django.views.decorators.csrf import csrf_exempt

def packet_list(request):
    # Fetch all packets from the database
    packets_list = Packet.objects.all().order_by('-timestamp')  # Order by timestamp descending

    # Handle page size
    items_per_page = int(request.GET.get('items_per_page', 100))  # Default to 100 if not specified
    max_pages = 5
    
    # Set up pagination
    paginator = Paginator(packets_list, items_per_page)
    page_number = request.GET.get('page', 1)  # Get the current page number from query parameters

    total_pages = paginator.num_pages
    if total_pages > max_pages:
        # Calculate the start and end pages to display
        start_page = max(1, int(page_number) - (max_pages // 2))
        end_page = min(total_pages, start_page + max_pages - 1)
        if end_page - start_page < max_pages - 1:
            start_page = max(1, end_page - max_pages + 1)
        page_range = range(start_page, end_page + 1)
    else:
        page_range = paginator.page_range

    page_obj = paginator.get_page(page_number)

    return render(request, 'network/dashboard.html', {
        'page_obj': page_obj,
        'page_range': page_range,  # Pass the page range to the template
        'items_per_page': items_per_page  # Pass the current page size to the template
    })

@csrf_exempt
def clear_and_capture(request):
    if request.method == "POST":
        # Clear all packets from the database
        Packet.objects.all().delete()

        # Define a callback function for packet capture
        def packet_callback(packet):
            Packet.objects.create(
                timestamp=datetime.now(),
                source_ip=packet[scapy.IP].src if scapy.IP in packet else '',
                destination_ip=packet[scapy.IP].dst if scapy.IP in packet else '',
                protocol=packet[scapy.IP].proto if scapy.IP in packet else '',
                length=len(packet),
                info=str(packet.summary())
            )

        # Start sniffing (example filter; adjust as needed)
        scapy.sniff(prn=packet_callback, filter="ip", count=100)  # Adjust count as needed

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'}, status=200)
    
    return HttpResponse("Invalid request method.", status=405)
