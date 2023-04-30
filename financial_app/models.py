
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class User:
#     pass

class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()

    def __str__(self):
        return self.name

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    investment_date = models.DateField()

    def __str__(self):
        return self.name

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Expense(models.Model):
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    shares = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

class Rebalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    target_allocation = models.DecimalField(max_digits=5, decimal_places=2)
    current_allocation = models.DecimalField(max_digits=5, decimal_places=2)
    rebalance_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}: {self.asset.name} Rebalance"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(
        max_length=10,
        choices=(('W', 'Weekly'), ('M', 'Monthly'), ('Y', 'Yearly')),
        default='M',
    )
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.source}"

class SpendingLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Spending Limit"

class SavingsPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title