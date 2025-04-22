"""from hash_it import *
from sql_zugriff import *
print(generate_normal_hash("A5ENUZHR"))
print(execute_get_query("SELECT OTP FROM User WHERE UserID = 1")[0][0])
print(generate_normal_hash("A5ENUZHR") == execute_get_query("SELECT OTP FROM User WHERE UserID = 1")[0][0])"""
def execute_python_string(code_string: str = """
def multiply(a, b):
    return a * b

result = multiply(4, 5)
print(result)
"""):
    compiled_code = compile(code_string, '<string>', 'exec')
    exec(compiled_code)
