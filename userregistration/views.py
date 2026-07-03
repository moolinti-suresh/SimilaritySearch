from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

from .forms import UserRegistrationForm
from .models import CustomUser
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST



CITY_STATE = {

    "Chennai": "Tamil Nadu",

    "Bangalore": "Karnataka",

    "Hyderabad": "Telangana",

    "Pune": "Maharashtra",
}


def register(request):

    if request.method == "POST":

        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():

            city = form.cleaned_data["city"]

            state = CITY_STATE[city]

            user = CustomUser(

                user_id=form.cleaned_data["user_id"],

                username=form.cleaned_data["username"],

                address=form.cleaned_data["address"],

                city=city,

                state=state,

                country=form.cleaned_data["country"],

                pin=form.cleaned_data["pin"],

                # File uploads
                aadhaar_file=request.FILES.get("aadhaar_file"),
                eb_bill_file=request.FILES.get("eb_bill_file"),

            )

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            messages.success(
                request,
                "User Registered Successfully."
            )

            return redirect("register")

    else:

        form = UserRegistrationForm()

    return render(
        request,
        "userregistration/register.html",
        {"form": form}
    )


def login_view(request):

    if request.method == "POST":

        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=user_id,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("search_users")
        else:
            return render(request, "login.html", {
                "error": "Invalid User ID or Password"
            })

    return render(request, "login.html")

@require_POST
def logout_view(request):
    logout(request)
    return redirect("register")


@login_required(login_url='login')
def search_users(request):

    address = request.GET.get("address", "").strip()

    page = int(request.GET.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    results = []
    total_records = 0

    if address:

        with connection.cursor() as cursor:

            # Count matching records
            cursor.execute("""
                SELECT COUNT(*)
                FROM userregistration_customuser
                WHERE similarity(full_address, %s) > 0;
            """, [address])

            total_records = cursor.fetchone()[0]

            # Fetch only one page
            cursor.execute("""
                SELECT
                    user_id,
                    username,
                    similarity(full_address, %s) * 100 AS match_percentage
                FROM userregistration_customuser
                WHERE similarity(full_address, %s) > 0
                ORDER BY match_percentage DESC
                LIMIT %s OFFSET %s;
            """, [address, address, per_page, offset])

            columns = [col[0] for col in cursor.description]

            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

    paginator = Paginator(range(total_records), per_page)

    page_obj = paginator.get_page(page)

    # Replace dummy objects with actual results
    page_obj.object_list = results

    # -------------------------------
    # Show only 5 page numbers
    # -------------------------------
    current_page = page_obj.number

    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(
        request,
        "userregistration/search_similar_users.html",
        {
            "page_obj": page_obj,
            "page_range": page_range,
            "address": address,
            "total_records": total_records,
        },
    )


def user_details(request, user_id):
    address = request.GET.get("address", "")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                user_id,
                username,
                address,
                state,
                city,
                full_address,
                aadhaar_file,
                eb_bill_file,
                similarity(full_address, %s) * 100 AS match_percentage
            FROM userregistration_customuser
            WHERE user_id = %s;
        """, [address, user_id])

        row = cursor.fetchone()
        if row:
            user = {
                "user_id": row[0],
                "username": row[1],
                "address": row[2],
                "state": row[3],
                "city": row[4],
                "full_address": row[5],
                "aadhaar_file": row[6],
                "eb_bill_file": row[7],
                "match_percentage": row[8],
            }
        else:
            user = None

    return render(request, "user_details.html", {"user": user})

   