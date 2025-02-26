# conversie din model data in JSON
from rest_framework import serializers
from .models import Event, Order

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'  # Serialize all fields

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # Serialize all fields