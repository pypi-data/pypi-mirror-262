# zpyval - Python Value Validator

## Overview

zpyval is a Python package designed to facilitate the validation of 
various types of values in Python programs. It provides a simple and 
intuitive interface to validate inputs according to specified criteria, 
allowing developers to ensure data integrity and 
consistency within their applications.

## Installation
You can install zpyval via pip:

```bash
pip install zpyval
```

## Usage

Using zpyval is straightforward. Simply import the required `Value` class you 
need and instantiate it with the real value. It checks the validation criteria 
on the fly. Returns object if validation passes otherwise raises a `ValueError`
with the corresponding message.

Here's a basic example:

```python
from zpyval.value import Username, Age, Gender

class User:
    def __init__(self, username, age, gender):
        self.username = username
        self.age = age
        self.gender = gender

user = User(Username('zatha'), Age(23), Gender('male'))

print(user.username.value, user.username()) # get value by property or __call__
print(user.gender())
print(user.age(), user.age.is_adult())
```

You don't need to worry about data validation and constraints at any point. 
Additionally, it offers special value object-based utility methods.