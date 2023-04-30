from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('goals/', views.goals, name='goals'),
    path('goals/add/', views.add_goal, name='add_goal'),
    path('investments/', views.investments, name='investments'),
    path('investments/add/', views.add_investment, name='add_investment'),
    path('budget/', views.budget, name='budget'),
    path('budget/add/', views.add_expense, name='add_expense'),
    path('alerts/', views.alerts, name='alerts'),
    path('resources/', views.resources, name='resources'),
    path('portfolio_analysis/', views.portfolio_analysis, name='portfolio_analysis'),
    path('rebalance_portfolio/', views.rebalance_portfolio, name='rebalance_portfolio'),
    path('cash_flow/', views.cash_flow, name='cash_flow'),
    path('goal_progress/', views.goal_progress, name='goal_progress'),
    path('financial_overview/', views.financial_overview, name='financial_overview'),
    path('investment_performance/', views.investment_performance, name='investment_performance'),
    path('expense_analysis/', views.expense_analysis, name='expense_analysis'),
    path('incomes/', views.incomes, name='incomes'),
    path('add_income/', views.add_income, name='add_income'),
    path('edit_income/<int:income_id>/', views.edit_income, name='edit_income'),
    path('delete_income/<int:income_id>/', views.delete_income, name='delete_income'),
    path('analytics/', views.analytics, name='analytics'),
    path('spending_limit/', views.spending_limit, name='spending_limit'),
    path('savings_plan/create/', views.create_savings_plan, name='create_savings_plan'),
    path('savings_plan/edit/<int:savings_plan_id>/', views.edit_savings_plan, name='edit_savings_plan'),
    # Add more URL patterns for other views here
]
