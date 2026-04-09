import datetime

import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import SpaBooking

def home(request):
    return render(request, "index.html")


def thank_you(request):
    return render(request, "thank_you.html")


def book_spa(request):
    if request.method != "POST":
        return redirect("home")

    full_name = request.POST.get("full_name", "").strip()
    phone_number = request.POST.get("phone_number", "").strip()
    email_address = request.POST.get("email_address", "").strip()
    selected_service = request.POST.get("selected_service", "").strip()
    service_for = request.POST.get("service_for", "").strip()
    preferred_date_raw = request.POST.get("preferred_date", "").strip()
    preferred_time_raw = request.POST.get("preferred_time", "").strip()
    special_request = request.POST.get("special_request", "").strip()
    privacy_policy_agreement = request.POST.get("privacy_policy_agreement") == "on"

    if not all([full_name, phone_number, selected_service, service_for, preferred_date_raw]):
        messages.error(request, "Please complete all required booking fields.")
        return redirect(f"{reverse('home')}#book")

    try:
        preferred_date = datetime.date.fromisoformat(preferred_date_raw)
    except ValueError:
        messages.error(request, "Please provide a valid preferred date.")
        return redirect(f"{reverse('home')}#book")

    preferred_time = None
    if preferred_time_raw:
        try:
            preferred_time = datetime.time.fromisoformat(preferred_time_raw)
        except ValueError:
            messages.error(request, "Please provide a valid preferred time.")
            return redirect(f"{reverse('home')}#book")

    booking = SpaBooking.objects.create(
        full_name=full_name,
        phone_number=phone_number,
        email_address=email_address,
        selected_service=selected_service,
        service_for=service_for,
        preferred_date=preferred_date,
        preferred_time=preferred_time,
        message=special_request,
        privacy_policy_agreement=privacy_policy_agreement,
    )

    sent = _send_booking_email(booking)
    if sent:
        messages.success(request, "Thank you. Your booking request was received.")
    else:
        messages.warning(
            request,
            "Your booking was saved, but email notification could not be sent.",
        )

    return redirect("thank_you")


def _send_booking_email(booking: SpaBooking) -> bool:
    if not settings.RESEND_API_KEY or not settings.RESEND_FROM or not settings.BOOKING_ALERT_EMAIL:
        return False

    preferred_time = booking.preferred_time.strftime("%H:%M") if booking.preferred_time else "Not specified"
    message = booking.message if booking.message else "No special request."

    html = f"""
    <h2>New Spa Booking</h2>
    <p><strong>Full Name:</strong> {booking.full_name}</p>
    <p><strong>Phone:</strong> {booking.phone_number}</p>
    <p><strong>Email:</strong> {booking.email_address or 'Not provided'}</p>
    <p><strong>Select Service:</strong> {booking.selected_service}</p>
    <p><strong>Who is this service for:</strong> {booking.get_service_for_display()}</p>
    <p><strong>Preferred Date:</strong> {booking.preferred_date.isoformat()}</p>
    <p><strong>Preferred Time:</strong> {preferred_time}</p>
    <p><strong>Special Request:</strong> {message}</p>
    <p><strong>Privacy Policy Agreement:</strong> {'Yes' if booking.privacy_policy_agreement else 'No'}</p>
    """

    payload = {
        "from": settings.RESEND_FROM,
        "to": [settings.BOOKING_ALERT_EMAIL],
        "subject": "New Spa Booking Request",
        "html": html,
    }
    if settings.RESEND_REPLY_TO:
        payload["reply_to"] = settings.RESEND_REPLY_TO

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=12,
        )
        return response.status_code in (200, 201)
    except requests.RequestException:
        return False