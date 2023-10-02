from django.db import models
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_url = 'sqlite:///C:/pythonProject23/myproject/example.db'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# Определение модели
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


# Создание таблицы в базе данных
Base.metadata.create_all(engine)


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    objects = models.Manager()


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    objects = models.Manager()


class Order(models.Model):
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ № {self.pk} - Client: {self.customer.name}"

    objects = models.Manager()


class OrderProduct(models.Model):
    order_ref = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_ref = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Товар: {self.product_ref.name} - Количество: {self.quantity}"

    objects = models.Manager()
