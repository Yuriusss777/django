from django import forms
from .models import Client, Product, Order


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'quantity', 'photo']

    photo = forms.FileField(required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'products', 'total_amount']

    def clean_total_amount(self):
        total_amount = self.cleaned_data['total_amount']
        if total_amount <= 0:
            raise forms.ValidationError("Общая сумма заказа должна быть положительным числом.")
        return total_amount
