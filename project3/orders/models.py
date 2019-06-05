from django.db import models

# Create your models here.
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

class PizzaTopping(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"

class Pizza(models.Model):
    pizza_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(PizzaTopping, blank=True)
    size = models.CharField(max_length=2, choices=(("sm", "small"), ("lg", "large")), default="sm")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_price(self):
        num_toppings = self.toppings.all().count()
        if num_toppings > 3:
            num_toppings = "special"
        self.price = eval("self.pizza_type." +
                          str(self.size) +
                          "_topping_" +
                          str(num_toppings))

    def __str__(self):
        return f"{self.pizza_type.name} with {self.toppings.all().count()} toppings"

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

class SubTopping(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price_sm = models.DecimalField(max_digits=6, decimal_places=2)
    price_lg = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}: small - ${self.price_sm}, large - ${self.price_lg}"

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
