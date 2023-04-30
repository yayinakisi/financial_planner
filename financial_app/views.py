from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investment, Alert, Resource, ExpenseCategory, Expense, FinancialGoal, Portfolio, Stock, Rebalance, Income, SpendingLimit, SavingsPlan
from .forms import ExpenseCategoryForm, ExpenseForm, IncomeForm, SpendingLimitForm, SavingsPlanForm
from alpha_vantage.timeseries import TimeSeries
import os
from django.db.models import Sum
import plotly.graph_objs as go
import plotly.express as px
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
from decimal import Decimal

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            auth_login(request, user)  # Use auth_login instead of login
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'financial_app/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'financial_app/login.html')

@login_required
def dashboard(request):
    goals = FinancialGoal.objects.filter(user=request.user)
    investments = Investment.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    context = {
        'goals_count': goals.count(),
        'investments_count': investments.count(),
        'expenses_count': expenses.count(),
    }

    return render(request, 'financial_app/dashboard.html', context)


@login_required
def goals(request):
    user_goals = FinancialGoal.objects.filter(user=request.user)
    return render(request, 'financial_app/goals.html', {'goals': user_goals})

@login_required
def add_goal(request):
    if request.method == 'POST':
        goal_name = request.POST['goal_name']
        goal_amount = request.POST['goal_amount']
        goal_deadline = request.POST['goal_date']

        goal = FinancialGoal(
            user=request.user,
            name=goal_name,
            amount=goal_amount,
            deadline=goal_deadline,
        )
        goal.save()
        messages.success(request, 'Goal added successfully!')
        return redirect('goals')
    else:
        return redirect('goals')


@login_required
def investments(request):
    user_investments = Investment.objects.filter(user=request.user)
    return render(request, 'financial_app/investments.html', {'investments': user_investments})

@login_required
def add_investment(request):
    if request.method == 'POST':
        name = request.POST['investment_name']
        amount = request.POST['investment_amount']
        investment_date = request.POST['investment_date']

        investment = Investment(user=request.user, name=name, amount=amount, investment_date=investment_date)
        investment.save()

        return redirect('investments')

    return HttpResponseRedirect(reverse('investments'))

from django.contrib.auth.decorators import login_required


@login_required
def budget(request):
    user_expenses = Expense.objects.filter(user=request.user)
    return render(request, 'financial_app/budget.html', {'expenses': user_expenses})

@login_required
def add_expense(request):
    if request.method == 'POST':
        name = request.POST['expense_name']
        amount = request.POST['expense_amount']
        expense_date = request.POST['expense_date']

        expense = Expense(user=request.user, name=name, amount=amount, expense_date=expense_date)
        expense.save()

        return redirect('budget')

    return HttpResponseRedirect(reverse('budget'))

def index(request):
    return render(request, 'financial_app/index.html')

@login_required
def alerts(request):
    user_alerts = Alert.objects.filter(user=request.user).order_by('-timestamp')
    context = {'alerts': user_alerts}
    return render(request, 'financial_app/alerts.html', context)

def resources(request):
    resources = Resource.objects.all()
    context = {'resources': resources}
    return render(request, 'financial_app/resources.html', context)

def expense_categories(request):
    categories = ExpenseCategory.objects.filter(user=request.user)
    return render(request, 'financial_app/expense_categories.html', {'categories': categories})

def investment_performance(request):
    investments = Investment.objects.filter(user=request.user)
    benchmarks = Benchmark.objects.all()
    return render(request, 'financial_app/investment_performance.html', {'investments': investments, 'benchmarks': benchmarks})

def expense_analysis(request):
    categories = ExpenseCategory.objects.filter(user=request.user)
    category_expenses = []
    
    for category in categories:
        total_expense = Expense.objects.filter(user=request.user, category=category).aggregate(Sum('amount'))['amount__sum'] or 0
        category_expenses.append({'category': category, 'total_expense': total_expense})
    
    return render(request, 'financial_app/expense_analysis.html', {'category_expenses': category_expenses})

# @login_required
# def portfolio_analysis(request):
#     portfolio = Portfolio.objects.get(user=request.user)
#     stocks = Stock.objects.filter(portfolio=portfolio)

#     api_key = os.environ.get("XR8Y8NQCTXZRG1HQ")
#     ts = TimeSeries(key=api_key)

#     stock_data = []
#     total_value = 0

#     for stock in stocks:
#         data, _ = ts.get_quote_endpoint(symbol=stock.symbol)
#         price = float(data["05. price"])
#         value = price * stock.shares
#         total_value += value

#         stock_data.append({
#             "symbol": stock.symbol,
#             "shares": stock.shares,
#             "purchase_price": stock.purchase_price,
#             "current_price": price,
#             "value": value,
#         })

#     context = {
#         "stock_data": stock_data,
#         "total_value": total_value,
#     }

#     return render(request, "financial_app/portfolio_analysis.html", context)
@login_required
def portfolio_analysis(request):
    try:
        portfolio = Portfolio.objects.filter(user=request.user).get()
    except Portfolio.DoesNotExist:
        error_message = "You do not have a portfolio."
        context = {"error_message": error_message}
        return render(request, "financial_app/portfolio_analysis.html", context)

    stocks = Stock.objects.filter(portfolio=portfolio)

    api_key = os.environ.get("XR8Y8NQCTXZRG1HQ")
    ts = TimeSeries(key=api_key)

    stock_data = []
    total_value = 0

    for stock in stocks:
        data, _ = ts.get_quote_endpoint(symbol=stock.symbol)
        price = float(data["05. price"])
        value = price * stock.shares
        total_value += value

        stock_data.append({
            "symbol": stock.symbol,
            "shares": stock.shares,
            "purchase_price": stock.purchase_price,
            "current_price": price,
            "value": value,
        })

    context = {
        "stock_data": stock_data,
        "total_value": total_value,
    }

    return render(request, "financial_app/portfolio_analysis.html", context)

def rebalance_portfolio(request):
    if request.method == 'POST':
        form = Rebalance(request.POST)
        if form.is_valid():
            rebalance = form.save(commit=False)
            rebalance.user = request.user
            rebalance.save()
            messages.success(request, 'Portfolio rebalanced successfully!')
            return redirect('portfolio_analysis')
    else:
        form = Rebalance()
    return render(request, 'financial_app/rebalance_portfolio.html', {'form': form})

def cash_flow(request):
    income = Investment.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    cash_flow = income - expenses
    return render(request, 'financial_app/cash_flow.html', {'cash_flow': cash_flow, 'income': income, 'expenses': expenses})

def goal_progress(request):
    goals = FinancialGoal.objects.filter(user=request.user)
    goal_data = []
    for goal in goals:
        progress = Investment.objects.filter(user=request.user, investment_goal=goal).aggregate(Sum('amount'))['amount__sum'] or 0
        goal_data.append({
            'goal': goal,
            'progress': progress,
            'percentage': (progress / goal.amount) * 100
        })
    return render(request, 'financial_app/goal_progress.html', {'goal_data': goal_data})

def financial_overview(request):
    income = Income.objects.filter(user=request.user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    expenses = Expense.objects.filter(user=request.user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    savings = []
    for i, expense in enumerate(expenses):
        income_month = next((x for x in income if x['month'] == expense['month']), None)
        if income_month:
            savings.append({'month': expense['month'], 'total': income_month['total'] - expense['total']})

    return render(request, 'financial_app/financial_overview.html', {'income': income, 'expenses': expenses, 'savings': savings})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('expenses')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'financial_app/add_expense.html', {'form': form})


def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(request, 'financial_app/edit_expense.html', {'form': form, 'expense': expense})

def incomes(request):
    user_incomes = Income.objects.filter(user=request.user).order_by('-date_added')
    context = {'incomes': user_incomes}
    return render(request, 'financial_app/incomes.html', context)

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('incomes')
    else:
        form = IncomeForm()
    return render(request, 'financial_app/add_income.html', {'form': form})

def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('incomes')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'financial_app/edit_income.html', {'form': form, 'income': income})

def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    income.delete()
    return redirect('incomes')

def analytics(request):
    # Query user's financial data
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    investments = Investment.objects.filter(user=request.user)

    # Create visualizations
    income_fig = px.pie(incomes, values='amount', names='source', title='Income Breakdown')
    expense_fig = px.pie(expenses, values='amount', names='category', title='Expense Breakdown')
    investment_fig = px.bar(investments, x='name', y='current_value', title='Investment Portfolio')

    # Combine the visualizations into a single dashboard
    dashboard = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "bar"}]])
    dashboard.add_trace(income_fig.data[0], row=1, col=1)
    dashboard.add_trace(expense_fig.data[0], row=1, col=2)
    dashboard.add_trace(investment_fig.data[0], row=1, col=3)

    # Render the dashboard in a Django template
    div = dashboard.to_html(full_html=False)
    return render(request, 'financial_app/analytics.html', {'dashboard': div})

def spending_limit(request):
    try:
        spending_limit = SpendingLimit.objects.get(user=request.user)
    except SpendingLimit.DoesNotExist:
        spending_limit = None

    if request.method == 'POST':
        form = SpendingLimitForm(request.POST, instance=spending_limit)
        if form.is_valid():
            spending_limit = form.save(commit=False)
            spending_limit.user = request.user
            spending_limit.save()
            return redirect('dashboard')
    else:
        form = SpendingLimitForm(instance=spending_limit)

    expenses = Expense.objects.filter(user=request.user)
    total_expenses = sum(expense.amount for expense in expenses)

    if spending_limit:
        progress = (total_expenses / spending_limit.monthly_limit) * 100
    else:
        progress = 0

    context = {
        'form': form,
        'progress': progress,
        'total_expenses': total_expenses,
    }
    return render(request, 'financial_app/spending_limit.html', context)

def create_savings_plan(request):
    if request.method == 'POST':
        form = SavingsPlanForm(request.POST)
        if form.is_valid():
            savings_plan = form.save(commit=False)
            savings_plan.user = request.user
            savings_plan.save()
            return redirect('dashboard')
    else:
        form = SavingsPlanForm()
    return render(request, 'financial_app/create_savings_plan.html', {'form': form})

def edit_savings_plan(request, savings_plan_id):
    savings_plan = get_object_or_404(SavingsPlan, id=savings_plan_id, user=request.user)
    if request.method == 'POST':
        form = SavingsPlanForm(request.POST, instance=savings_plan)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SavingsPlanForm(instance=savings_plan)
    return render(request, 'financial_app/edit_savings_plan.html', {'form': form})