import os, sys
sys.path.append("/Users/ChiChi/Desktop/workspace/cs50_web/project3")
os.environ['DJANGO_SETTINGS_MODULE'] = 'pizza.settings'

import django
django.setup()

from orders.models import *

def populate():

    pizza_types = [
        {
            "name": "Regular Pizza",
            "sm_topping_0": 12.20,
            "sm_topping_1": 13.20,
            "sm_topping_2": 14.70,
            "sm_topping_3": 15.70,
            "sm_topping_special": 17.25,
            "lg_topping_0": 17.45,
            "lg_topping_1": 19.45,
            "lg_topping_2": 21.45,
            "lg_topping_3": 23.45,
            "lg_topping_special": 25.45
            },
        {
            "name": "Sicilian Pizza",
            "sm_topping_0": 23.45,
            "sm_topping_1": 25.45,
            "sm_topping_2": 27.45,
            "sm_topping_3": 28.45,
            "sm_topping_special": 29.45,
            "lg_topping_0": 37.70,
            "lg_topping_1": 39.70,
            "lg_topping_2": 41.70,
            "lg_topping_3": 43.70,
            "lg_topping_special": 44.70
            },
        ]

    pizza_toppings = [
        "Pepperoni",
        "Sausage",
        "Mushrooms",
        "Onions",
        "Ham",
        "Canadian Bacon",
        "Pineapple",
        "Eggplant",
        "Tomato & Basil",
        "Green Peppers",
        "Hamburger",
        "Spinach",
        "Artichoke",
        "Buffalo Chicken",
        "Barbecue Chicken",
        "Anchovies",
        "Black Olives",
        "Fresh Garlic",
        "Zucchini",
        ]

    sub_toppings = [
        {"name": "Mushrooms", "price_sm": 0.50, "price_lg": 0.50},
        {"name": "Green Peppers", "price_sm": 0.50, "price_lg": 0.50},
        {"name": "Onions", "price_sm": 0.50, "price_lg": 0.50},
        {"name": "Cheese", "price_sm": 0.50, "price_lg": 0.50}
        ]

    sub_types = [
        {"name": "Cheese", "price_sm": 6.50, "price_lg": 7.95},
        {"name": "Italian", "price_sm": 6.50, "price_lg": 7.95},
        {"name": "Ham + Cheese", "price_sm": 6.50, "price_lg": 7.95},
        {"name": "Meatball", "price_sm": 6.50, "price_lg": 7.95},
        {"name": "Tuna", "price_sm": 6.50, "price_lg": 7.95},
        {"name": "Turkey", "price_sm": 7.50, "price_lg": 8.50},
        {"name": "Chicken Parmigiana", "price_sm": 7.50, "price_lg": 8.50},
        {"name": "Eggplant Parmigiana", "price_sm": 6.50, "price_lg": 7.95},
        {"name": "Steak", "price_sm": 6.50, "price_lg": 7.95},
        {"name": "Steak + Cheese", "price_sm": 6.95, "price_lg": 8.50},
        {"name": "Sausage, Peppers & Onions", "price_sm": None, "price_lg": 7.95},
        {"name": "Hamburger", "price_sm": 4.60, "price_lg": 6.95},
        {"name": "Cheeseburger", "price_sm": 5.10, "price_lg": 7.45},
        {"name": "Fried Chicken", "price_sm": 6.95, "price_lg": 8.50},
        {"name": "Veggie", "price_sm": 6.95, "price_lg": 8.50}
        ]

    pasta_types = [
        {"name": "Baked Ziti w/Mozzarella", "price": 6.50},
        {"name": "Baked Ziti w/Meatballs", "price": 8.75},
        {"name": "Baked Ziti w/Chicken", "price": 9.75}
        ]

    salad_types = [
        {"name": "Garden Salad", "price": 6.25},
        {"name": "Greek Salad", "price": 8.25},
        {"name": "Antipasto", "price": 8.25},
        {"name": "Salad w/Tuna", "price": 8.25}
        ]

    platter_types = [
        {"name": "Garden Salad", "price_sm": 35.00, "price_lg": 60.00},
        {"name": "Greek Salad", "price_sm": 45.00, "price_lg": 70.00},
        {"name": "Antipasto", "price_sm": 45.00, "price_lg": 70.00},
        {"name": "Baked Ziti", "price_sm": 35.00, "price_lg": 60.00},
        {"name": "Meatball Parm", "price_sm": 45.00, "price_lg": 70.00},
        {"name": "Chicken Parm", "price_sm": 45.00, "price_lg": 80.00}
        ]

    # Add pizza types
    PizzaType.objects.all().delete()
    for p in pizza_types:
        new_type = PizzaType(name=p["name"],
                             sm_topping_0=p["sm_topping_0"],
                             sm_topping_1=p["sm_topping_1"],
                             sm_topping_2=p["sm_topping_2"],
                             sm_topping_3=p["sm_topping_3"],
                             sm_topping_special=p["sm_topping_special"],
                             lg_topping_0=p["lg_topping_0"],
                             lg_topping_1=p["lg_topping_1"],
                             lg_topping_2=p["lg_topping_2"],
                             lg_topping_3=p["lg_topping_3"],
                             lg_topping_special=p["lg_topping_special"])
        new_type.save()
        print(f"Added {new_type.name} to PizzaType")

    # Add all toppings
    PizzaTopping.objects.all().delete()
    for t in pizza_toppings:
        new_topping = PizzaTopping(name=t)
        new_topping.save()
        print(f"Added {new_topping.name} to PizzaTopping")

    # Add all sub toppings
    SubTopping.objects.all().delete()
    for t in sub_toppings:
        new_topping = SubTopping(name=t["name"], price_sm=t["price_sm"], price_lg=t["price_lg"])
        new_topping.save()
        print(f"Added {new_topping.name} to SubTopping")

    # Add all sub types
    SubType.objects.all().delete()
    for t in sub_types:
        new_subtype = SubType(name=t["name"], price_sm=t["price_sm"], price_lg=t["price_lg"])
        new_subtype.save()
        print(f"Added {new_subtype.name} to SubType")

    # Add all pastas
    PastaType.objects.all().delete()
    for p in pasta_types:
        new_pasta = PastaType(name=p["name"], price=p["price"])
        new_pasta.save()
        print(f"Added {new_pasta.name} to PastaType")

    # Add all salads
    SaladType.objects.all().delete()
    for s in salad_types:
        new_salad = SaladType(name=s["name"], price=s["price"])
        new_salad.save()
        print(f"Added {new_salad.name} to SaladType")

    # Add all platters
    PlatterType.objects.all().delete()
    for p in platter_types:
        new_platter = PlatterType(name=p["name"], price_sm=p["price_sm"], price_lg=p["price_lg"])
        new_platter.save()
        print(f"Added {new_platter.name} to PlatterType")

if __name__ == "__main__":
    populate()
