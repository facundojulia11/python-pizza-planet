
def calculate_ingredients_total_amount(ingredients):
    return sum(ingredient.price for ingredient in ingredients)

def calculate_beverages_total_amount(beverages):
    return sum(beverage.price for beverage in beverages)