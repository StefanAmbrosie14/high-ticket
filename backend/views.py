from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Event, Order
from .serializers import EventSerializer, OrderSerializer

#get all event
@api_view(['GET'])
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

#get single event
@api_view(['GET'])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

#get all orders
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

#get single order
@api_view(['GET'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
