import random

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from userregistration.models import CustomUser


class Command(BaseCommand):
    help = "Generate 100000 test users"

    def handle(self, *args, **kwargs):

        cities = {
            "Chennai": "Tamil Nadu",
            "Bangalore": "Karnataka",
            "Hyderabad": "Telangana",
            "Pune": "Maharashtra",
        }

        streets = [
            "Anna Nagar",
            "MG Road",
            "T Nagar",
            "Brigade Road",
            "JP Nagar",
            "Banjara Hills",
            "Ameerpet",
            "Velachery",
            "Adyar",
            "Koramangala",
        ]

        password = make_password("admin123")

        users = []

        start_id = 200001
        total_users = 500000
        batch_size = 5000

        for i in range(total_users):

            user_id = start_id + i

            city = random.choice(list(cities.keys()))
            state = cities[city]

            house_no = random.randint(1, 999)

            street = random.choice(streets)

            pin = str(random.randint(100000, 999999))

            address = f"{house_no}, {street}"

            full_address = (
                f"{address}, "
                f"{city}, "
                f"{state}, "
                f"India - {pin}"
            )

            users.append(
                CustomUser(
                    user_id=user_id,
                    username=f"user{user_id}",
                    password=password,
                    address=address,
                    city=city,
                    state=state,
                    country="India",
                    pin=pin,
                    full_address=full_address,
                    aadhaar_file=None,
                    eb_bill_file=None,
                    is_active=True,
                    is_staff=False,
                )
            )

            if len(users) == batch_size:
                CustomUser.objects.bulk_create(users)
                self.stdout.write(f"Inserted {user_id}")
                users = []

        if users:
            CustomUser.objects.bulk_create(users)

        self.stdout.write(
            self.style.SUCCESS("100000 users created successfully.")
        )