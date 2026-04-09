from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SpaBooking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=140)),
                ("phone_number", models.CharField(max_length=40)),
                ("email_address", models.EmailField(blank=True, max_length=254)),
                ("selected_service", models.CharField(max_length=120)),
                (
                    "service_for",
                    models.CharField(
                        choices=[
                            ("myself", "Myself"),
                            ("someone_else", "Someone else"),
                            ("couple", "Couple"),
                        ],
                        max_length=20,
                    ),
                ),
                ("preferred_date", models.DateField()),
                ("preferred_time", models.TimeField(blank=True, null=True)),
                ("message", models.TextField(blank=True)),
                ("privacy_policy_agreement", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
