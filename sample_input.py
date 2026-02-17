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