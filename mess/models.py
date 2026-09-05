from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Menu(models.Model):
    date = models.DateField()
    breakfast = models.CharField(max_length=200)
    lunch = models.CharField(max_length=200)
    dinner = models.CharField(max_length=200)

    def __str__(self):
        return str(self.date)


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.date}"


class Complaint(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    priority = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.priority}"


# ✅ KEEP ONLY ONE (Rating)
class Rating(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()   # 1–5
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.stars}⭐"


class Bill(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.student.username} - {self.month}"


class AllowedStudent(models.Model):
    admission_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.admission_number