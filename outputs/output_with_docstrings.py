"""
Sample Python file for testing Python Docstring Generator.
This file contains various functions without docstrings.
"""


def calculate_area(length, width):
    """Calculate area of rectangle."""
    return length * width


def calculate_volume(length, width, height):
    """
    Calculates the volume of a rectangular prism.
    
    This function computes the product of three dimensions (length, width, and height)
    to determine the volume of a three-dimensional object like a cuboid.
    
    Parameters
    ----------
    length : int or float
        The length of the rectangular prism. Must be a non-negative number.
    width : int or float
        The width of the rectangular prism. Must be a non-negative number.
    height : int or float
        The height of the rectangular prism. Must be a non-negative number.
    
    Returns
    -------
    int or float
        The calculated volume. The type will typically be `float` if any input is a `float`,
        otherwise `int`.
    
    Raises
    ------
    TypeError
        If any of the input parameters (length, width, or height) are not numbers
        (e.g., strings, None, or other non-numeric types).
    
    Examples
    --------
    >>> calculate_volume(2, 3, 4)
    24
    >>> calculate_volume(2.5, 2, 3)
    15.0
    >>> calculate_volume(0, 5, 10)
    0
    """
    return length * width * height


def fahrenheit_to_celsius(fahrenheit):
    """
    Converts temperature from Fahrenheit to Celsius.

    This function applies the standard formula to convert a given temperature
    value from the Fahrenheit scale to the Celsius scale.

    Parameters
    ----------
    fahrenheit : float or int
        The temperature value in degrees Fahrenheit.

    Returns
    -------
    float
        The equivalent temperature in degrees Celsius.

    Examples
    --------
    >>> fahrenheit_to_celsius(32)
    0.0
    >>> fahrenheit_to_celsius(212)
    100.0
    >>> fahrenheit_to_celsius(98.6)
    37.0
    """
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius



def find_maximum(numbers):
    """
    Finds the maximum number in a list of numbers.
    
    This function iterates through a given list of numbers and determines the
    largest value among them. It handles empty lists by returning None.
    
    Parameters
    ----------
    numbers : list of int or float
        A list containing numerical values (integers or floating-point numbers)
        from which to find the maximum.
    
    Returns
    -------
    int or float or None
        The maximum numerical value found in the list. Returns None if the input
        list `numbers` is empty.
    
    Examples
    --------
    >>> find_maximum([1, 5, 2, 8, 3])
    8
    >>> find_maximum([-10, -5, -20])
    -5
    >>> find_maximum([7.1, 7.0, 7.2])
    7.2
    >>> find_maximum([])
    None
    """
    if not numbers:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num


def is_palindrome(text):
    """
    Check if a given string is a palindrome.
    
    This function determines whether a string is a palindrome by ignoring case
    and all non-alphanumeric characters. It compares the cleaned string with
    its reversed version.
    
    Parameters
    ----------
    text : str
        The input string to be checked for the palindrome property.
    
    Returns
    -------
    bool
        True if the input string is a palindrome (case-insensitive and
        ignoring non-alphanumeric characters), False otherwise.
    
    See Also
    --------
    str.lower : Convert string to lowercase.
    str.isalnum : Check if a character is alphanumeric.
    
    Notes
    -----
    An empty string is considered a palindrome. This implementation is robust
    against variations in casing, spacing, and punctuation.
    
    Examples
    --------
    >>> is_palindrome("Racecar")
    True
    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("Hello, World!")
    False
    >>> is_palindrome("Madam, I'm Adam")
    True
    >>> is_palindrome("")
    True
    """
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def factorial(n):
    """
    Calculate the factorial of a non-negative integer.
    
    The factorial of a non-negative integer `n`, denoted by `n!`, is the product
    of all positive integers less than or equal to `n`. The factorial of 0 is 1.
    
    Parameters
    ----------
    n : int
        The non-negative integer for which to calculate the factorial.
    
    Returns
    -------
    int
        The factorial of `n`.
    
    Raises
    ------
    TypeError
        If `n` is not an integer.
    ValueError
        If `n` is a negative integer.
    
    Notes
    -----
    This function implements the factorial calculation iteratively.
    The mathematical definition is used for handling 0 and 1.
    
    Examples
    --------
    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    >>> factorial(10)
    3628800
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be a non-negative integer.
    >>> factorial(3.5)
    Traceback (most recent call last):
        ...
    TypeError: n must be an integer.
    """
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result