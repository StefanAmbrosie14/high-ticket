from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# ----------------------------
# 1️⃣ USER & ORGANIZER MODELS
# ----------------------------

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer_profile')
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.organization_name or self.user.username

# ----------------------------
# 2️⃣ EVENT & IMAGES
# ----------------------------

class Event(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    hero_image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    is_featured = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.event.title}"

# ----------------------------
# 3️⃣ VIP MANAGEMENT
# ----------------------------

class VIPGuest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vip_profile')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='vip_guests')
    special_requests = models.TextField(blank=True, null=True)
    assigned_table = models.ForeignKey('TableReservation', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f"VIP {self.user.username} for {self.event.title}"

class TableReservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='table_reservations')
    table_name = models.CharField(max_length=255)
    number_of_seats = models.IntegerField()
    min_spend = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Table {self.table_name} for {self.event.title}"

# ----------------------------
# 4️⃣ DYNAMIC TICKETING
# ----------------------------

class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    allow_custom_requests = models.BooleanField(default=False)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class PriceWave(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='price_waves')
    ticket_count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class AddOn(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    assigned_table = models.ForeignKey(TableReservation, on_delete=models.SET_NULL, blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.unique_code} - {self.ticket_type.name}"

# ----------------------------
# 5️⃣ VENDOR MANAGEMENT
# ----------------------------

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=255)  # Catering, Security, etc.
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name

class VendorAssignment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='assignments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='vendor_assignments')
    task_description = models.TextField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    payment_status = models.BooleanField(default=False)

# ----------------------------
# 6️⃣ CHECK-IN & SECURITY
# ----------------------------

class CheckIn(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='checkin')
    checkin_time = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

class ConciergeRequest(models.Model):
    vip_guest = models.ForeignKey(VIPGuest, on_delete=models.CASCADE, related_name='concierge_requests')
    request_text = models.TextField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Handled', 'Handled')], default='Pending')
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

