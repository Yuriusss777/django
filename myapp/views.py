from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Product, Order, OrderProduct
from .forms import ClientForm, ProductForm, OrderForm
from django.views.generic import ListView
from datetime import datetime, timedelta
from django.utils import timezone


# Обработка создания клиента
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})


# Обработка чтения всех клиентов
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


# Обработка обновления клиента
def update_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'update_client.html', {'form': form})


# Обработка удаления клиента
def delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'delete_client.html', {'client': client})


# Обработка создания товара
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


# Обработка чтения всех товаров
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# Обработка обновления товара
def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form})


# Обработка удаления товара
def delete_product(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})


# # Обработка чтения всех заказов
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


# # Обработка обновления заказа
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'update_order.html', {'form': form})


# # Обработка удаления заказа
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'delete_order.html', {'order': order})


def client_orders(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    orders = Order.objects.filter(client=client)
    return render(request, 'client_orders.html', {'client': client, 'orders': orders})


class OrderProductListView(ListView):
    model = OrderProduct
    template_name = 'order_product_list.html'
    context_object_name = 'order_products'

    def get_queryset(self):
        return OrderProduct.objects.all()


def orders(request):
    # Получение дат для фильтрации
    today = datetime.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    last_year = today - timedelta(days=365)

    # Получение товаров за последнюю неделю
    recent_products = Order.objects.filter(order_date__gte=last_week, order_date__lte=today).values_list(
        'products__name', flat=True).distinct()

    # Получение товаров за последний месяц
    last_month_products = Order.objects.filter(order_date__gte=last_month, order_date__lte=today).values_list(
        'products__name', flat=True).distinct()

    # Получение товаров за последний год
    last_year_products = Order.objects.filter(order_date__gte=last_year, order_date__lte=today).values_list(
        'products__name', flat=True).distinct()

    return render(request, 'orders.html', {
        'recent_products': recent_products,
        'last_month_products': last_month_products,
        'last_year_products': last_year_products
    })


def client_ordered_products(request, client_id, period):
    client = Client.objects.get(pk=client_id)
    end_date = timezone.now()

    if period == 'неделя':
        start_date = end_date - timedelta(days=7)
    elif period == 'месяц':
        start_date = end_date - timedelta(days=30)
    elif period == 'год':
        start_date = end_date - timedelta(days=365)
    else:
        # По умолчанию, если не передан поддерживаемый период, используем месяц
        start_date = end_date - timedelta(days=30)

    client_orders_filtered = Order.objects.filter(customer=client, order_date__range=(start_date, end_date))
    ordered_products = Product.objects.filter(order__in=client_orders_filtered).distinct()

    return render(request, 'client_ordered_products.html', {
        'client': client,
        'ordered_products': ordered_products,
        'period': period,
    })

