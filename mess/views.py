from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from datetime import date

from .models import Menu, Complaint, Attendance, Bill, Rating


# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 Explicit check (more reliable)
            if user.is_superuser == True:
                return redirect('/admin-panel/')   # direct URL
            else:
                return redirect('/home/')          # direct URL

        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

# ================= STUDENT =================
@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def menu(request):
    menus = Menu.objects.all().order_by('-date')
    return render(request, 'menu.html', {'menus': menus})


@login_required
def attendance(request):
    return render(request, 'attendance.html')


# ✅ QR ATTENDANCE BACKEND (FIXED)
@login_required
@csrf_exempt
def mark_attendance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        meal = data.get("meal")

        today = timezone.now().date()

        attendance, created = Attendance.objects.get_or_create(
            student=request.user,
            date=today
        )

        if meal == "breakfast":
            attendance.breakfast = True
        elif meal == "lunch":
            attendance.lunch = True
        elif meal == "dinner":
            attendance.dinner = True

        attendance.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "failed"})


@login_required
def complaint(request):
    if request.method == "POST":
        message = request.POST.get('message')
        priority = request.POST.get('priority')

        Complaint.objects.create(
            student=request.user,
            message=message,
            priority=priority
        )

        return render(request, 'complaint.html', {'msg': 'Complaint submitted ✅'})

    return render(request, 'complaint.html')


@login_required
def rating(request):
    if request.method == "POST":
        stars = request.POST.get("stars")
        comment = request.POST.get("comment")

        Rating.objects.create(
            student=request.user,
            stars=int(stars),
            comment=comment
        )

        return redirect('rating')

    return render(request, 'rating.html')


# ✅ BILL CALCULATION (IMPROVED)
@login_required
def bill(request):
    today = date.today()

    # FILTER CURRENT MONTH
    records = Attendance.objects.filter(
        student=request.user,
        date__month=today.month,
        date__year=today.year
    )

    # COUNT MEALS
    breakfast_count = records.filter(breakfast=True).count()
    lunch_count = records.filter(lunch=True).count()
    dinner_count = records.filter(dinner=True).count()

    # PRICES
    PRICES = {
        "breakfast": 30,
        "lunch": 60,
        "dinner": 50
    }

    # TOTALS
    totals = {
        "breakfast": breakfast_count * PRICES["breakfast"],
        "lunch": lunch_count * PRICES["lunch"],
        "dinner": dinner_count * PRICES["dinner"],
    }

    # COST CALCULATION
    food_cost = sum(totals.values())
    prep_cost = int(food_cost * 0.2)
    maintenance = 500

    total = food_cost + prep_cost + maintenance

    context = {
        "counts": {
            "breakfast": breakfast_count,
            "lunch": lunch_count,
            "dinner": dinner_count,
        },
        "prices": PRICES,
        "totals": totals,
        "food_cost": food_cost,
        "prep_cost": prep_cost,
        "maintenance": maintenance,
        "total": total,
        "month": today.strftime("%B %Y")
    }

    return render(request, "bill.html", context)

# ================= ADMIN =================
@login_required
def admin_panel(request):

    if not request.user.is_superuser:
        return redirect('home')

    # ADD MENU
    if request.method == "POST":
        date = request.POST.get('date')
        breakfast = request.POST.get('breakfast')
        lunch = request.POST.get('lunch')
        dinner = request.POST.get('dinner')

        Menu.objects.create(
            date=date,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner
        )

    attendance = Attendance.objects.all().order_by('-date')
    complaints = Complaint.objects.all().order_by('-created_at')
    ratings = Rating.objects.all().order_by('-date')
    menu = Menu.objects.all().order_by('-date')

    # AVERAGE RATING
    avg_rating = 0
    if ratings.exists():
        avg_rating = sum(r.stars for r in ratings) / ratings.count()

    return render(request, 'admin.html', {
        'attendance': attendance,
        'complaints': complaints,
        'ratings': ratings,
        'menu': menu,
        'avg_rating': round(avg_rating, 1)
    })

from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'User already exists'})

        User.objects.create_user(username=username, password=password)

        return redirect('login')

    return render(request, 'register.html')