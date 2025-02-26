from django.contrib import admin
from .models import (
    User, Organizer, Event, EventImage, VIPGuest, TableReservation, 
    TicketType, PriceWave, AddOn, Order, Ticket, Vendor, VendorAssignment, 
    CheckIn, ConciergeRequest
)

# ----------------------------
# 1️⃣ USER & ORGANIZER ADMIN
# ----------------------------

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_organizer', 'is_staff', 'is_active')
    list_filter = ('is_organizer', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'phone')
    search_fields = ('organization_name', 'user__username', 'user__email')

# ----------------------------
# 2️⃣ EVENT MANAGEMENT
# ----------------------------

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_date', 'location')
    list_filter = ('start_date',)
    search_fields = ('title', 'organizer__user__username', 'location')
    inlines = [EventImageInline]

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image_url', 'is_featured')
    list_filter = ('event',)

# ----------------------------
# 3️⃣ VIP MANAGEMENT
# ----------------------------

@admin.register(VIPGuest)
class VIPGuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'assigned_table')
    search_fields = ('user__username', 'event__title')

@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'event', 'number_of_seats', 'reserved_by')
    list_filter = ('event',)
    search_fields = ('table_name', 'reserved_by__username')

# ----------------------------
# 4️⃣ TICKETING MANAGEMENT
# ----------------------------

class PriceWaveInline(admin.TabularInline):
    model = PriceWave
    extra = 1

class AddOnInline(admin.TabularInline):
    model = AddOn
    extra = 1

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'base_price', 'allow_custom_requests')
    list_filter = ('event',)
    search_fields = ('name', 'event__title')
    inlines = [PriceWaveInline, AddOnInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'total_amount', 'order_date')
    search_fields = ('user__username', 'event__title')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'order', 'ticket_type', 'assigned_table', 'issued_at')
    search_fields = ('unique_code', 'order__user__username', 'ticket_type__name')

# ----------------------------
# 5️⃣ VENDOR MANAGEMENT
# ----------------------------

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'contact_email', 'rating')
    search_fields = ('name', 'service_type')

@admin.register(VendorAssignment)
class VendorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'event', 'task_description', 'status', 'payment_status')
    list_filter = ('event', 'status', 'payment_status')
    search_fields = ('vendor__name', 'event__title')

# ----------------------------
# 6️⃣ CHECK-IN & SECURITY
# ----------------------------

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'checkin_time', 'verified_by')
    search_fields = ('ticket__unique_code', 'verified_by__username')

@admin.register(ConciergeRequest)
class ConciergeRequestAdmin(admin.ModelAdmin):
    list_display = ('vip_guest', 'request_text', 'status', 'handled_by')
    list_filter = ('status',)
    search_fields = ('vip_guest__user__username', 'request_text')

