def concat_with_space(a,b):
    return a + ' ' + b

print(concat_with_space('hello', 'world'))
print(concat_with_space('', ''))

def format_with_fstring(a,b):
    return f'Hello {a}, you are {b} years old'

print(format_with_fstring('John', 25))
print(format_with_fstring('Jane', 30))