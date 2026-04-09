from django.db import models


class SpaBooking(models.Model):
    RECIPIENT_CHOICES = [
        ("myself", "Myself"),
        ("someone_else", "Someone else"),
        ("couple", "Couple"),
    ]

    full_name = models.CharField(max_length=140)
    phone_number = models.CharField(max_length=40)
    email_address = models.EmailField(blank=True)
    selected_service = models.CharField(max_length=120)
    service_for = models.CharField(max_length=20, choices=RECIPIENT_CHOICES)
    preferred_date = models.DateField()
    preferred_time = models.TimeField(null=True, blank=True)
    message = models.TextField(blank=True)
    privacy_policy_agreement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.selected_service} ({self.preferred_date})"
