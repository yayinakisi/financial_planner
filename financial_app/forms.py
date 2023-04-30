from django import forms
from .models import ExpenseCategory, Expense, SpendingLimit, Income, SavingsPlan

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('source', 'amount', 'frequency')

class SpendingLimitForm(forms.ModelForm):
    class Meta:
        model = SpendingLimit
        fields = ('monthly_limit',)

class SavingsPlanForm(forms.ModelForm):
    class Meta:
        model = SavingsPlan
        fields = ['title', 'target_amount', 'target_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


