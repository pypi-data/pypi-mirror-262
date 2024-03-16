import re

def instance_of(value, klass, message=''):
    if not isinstance(value, klass):
        raise ValueError(message or f'value should be {klass.__name__}')
    

def is_true(cond, message):
    if not cond:
        raise ValueError(message)
    

def not_null(value):
    if value is None:
        raise ValueError('null value not allowed')
    

def contains(value, container):
    if value not in container:
        raise ValueError(f'value {value} not found in {container}')
    

def not_blank(value):
    if value == '':
        raise ValueError('value should not be blank')
    

def allow_null(value):
    return value is None

def not_null(value):
    if value is None:
        raise ValueError('value should not be null')
    
def matches_pattern(pattern, value, message):
    is_match = bool(re.match(pattern, value))
    if not is_match:
        raise ValueError(message)
    