from django.db import models

# Create your models here.

"""
Menu item types
----------------------------------------------------
"""

class PizzaType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    sm_topping_0 = models.DecimalField(max_digits=6, decimal_places=2)
    sm_topping_1 = models.DecimalField(max_digits=6, decimal_places=2)
    sm_topping_2 = models.DecimalField(max_digits=6, decimal_places=2)
    sm_topping_3 = models.DecimalField(max_digits=6, decimal_places=2)
    sm_topping_special = models.DecimalField(max_digits=6, decimal_places=2)
    lg_topping_0 = models.DecimalField(max_digits=6, decimal_places=2)
    lg_topping_1 = models.DecimalField(max_digits=6, decimal_places=2)
    lg_topping_2 = models.DecimalField(max_digits=6, decimal_places=2)
    lg_topping_3 = models.DecimalField(max_digits=6, decimal_places=2)
    lg_topping_special = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class SubType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price_sm = price_sm = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_lg = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        if self.price_sm is None:
            return f"{self.name}: small - None, large - ${self.price_lg:.2f}"
        elif self.price_lg is None:
            return f"{self.name}: small - ${self.price_sm:.2f}, large - None"
        else:
            return f"{self.name}: small - ${self.price_sm:.2f}, large - ${self.price_lg:.2f}"

class PastaType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}: ${self.price:.2f}"

class SaladType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}: ${self.price:.2f}"

class PlatterType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price_sm = models.DecimalField(max_digits=6, decimal_places=2)
    price_lg = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}: small - ${self.price_sm:.2f}, large - ${self.price_lg:.2f}"

"""
Toppings
----------------------------------------------------
"""
class PizzaTopping(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"

class SubTopping(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price_sm = models.DecimalField(max_digits=6, decimal_places=2)
    price_lg = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}: small - ${self.price_sm}, large - ${self.price_lg}"

"""
Order Items
----------------------------------------------------
"""
class Pizza(models.Model):
    type = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    size = models.CharField(max_length=2, choices=(("sm", "small"), ("lg", "large")), default="sm")
    toppings = models.ManyToManyField(PizzaTopping, blank=True)

    def calculate_price(self):
        num_toppings = self.toppings.all().count()
        if num_toppings > 3:
            num_toppings = "special"
        self.price = eval("self.type." +
                          str(self.size) +
                          "_topping_" +
                          str(num_toppings))
        self.save()

    def get_price(self):
        if self.price == 0.00:
            self.calculate_price()
        return self.price

    def __str__(self):
        return f"{self.size} {self.pizza_type.name} with {self.toppings.all().count()} toppings"

class Sub(models.Model):
    type = models.ForeignKey(SubType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    size = models.CharField(max_length=2, choices=(("sm", "small"), ("lg", "large")), default="sm")
    toppings = models.ManyToManyField(SubTopping, blank=True)

    def calculate_price(self):
        self.price = eval("self.type.price_" + str(self.size))
        for topping in self.toppings.all():
            self.price += eval("topping.price_" + str(self.size))
        self.save()

    def get_price(self):
        if self.price == 0.00:
            self.calculate_price()
        return self.price

    def __str__(self):
        return f"{self.size} {self.type.name} with {self.toppings.all().count()} add ons"

class Pasta(models.Model):
    type = models.ForeignKey(PastaType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_price(self):
        self.price = self.type.price
        self.save()

    def get_price(self):
        if self.price == 0.00:
            self.calculate_price()
        return self.price

    def __str__(self):
        return f"{self.type.name}: ${self.price:.2f}"

class Salad(models.Model):
    type = models.ForeignKey(PastaType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_price(self):
        self.price = self.type.price
        self.save()

    def get_price(self):
        if self.price == 0.00:
            self.calculate_price()
        return self.price

    def __str__(self):
        return f"{self.type.name}: ${self.price:.2f}"

class Platter(models.Model):
    type = models.ForeignKey(PastaType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    size = models.CharField(max_length=2, choices=(("sm", "small"), ("lg", "large")), default="sm")

    def calculate_price(self):
        self.price = eval("self.type.price_" + str(self.size))
        self.save()

    def get_price(self):
        if self.price == 0.00:
            self.calculate_price()
        return self.price

    def __str__(self):
        return f"{self.type.name}: ${self.price:.2f}"
