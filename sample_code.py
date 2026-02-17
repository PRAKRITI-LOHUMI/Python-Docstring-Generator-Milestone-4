"""
Sample Python file for testing Python Docstring Generator.
This file contains various functions without docstrings.
"""


def calculate_area(length, width):
    """Calculate area of rectangle."""
    return length * width


def calculate_volume(length, width, height):
    return length * width * height


def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius


def find_maximum(numbers):
    if not numbers:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num


def is_palindrome(text):
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def merge_lists(list1, list2):
    merged = []
    merged.extend(list1)
    merged.extend(list2)
    return sorted(merged)


class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        self.result = x + y
        return self.result
    
    def subtract(self, x, y):
        self.result = x - y
        return self.result
    
    def multiply(self, x, y):
        self.result = x * y
        return self.result
    
    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        self.result = x / y
        return self.result


def process_user_data(name, age, email, phone=None):
    user_info = {
        'name': name.strip().title(),
        'age': int(age),
        'email': email.lower(),
        'phone': phone
    }
    return user_info


def calculate_discount(price, discount_percentage):
    if discount_percentage < 0 or discount_percentage > 100:
        raise ValueError("Discount must be between 0 and 100")
    discount_amount = price * (discount_percentage / 100)
    final_price = price - discount_amount
    return final_price
