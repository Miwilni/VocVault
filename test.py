"""from hash_it import *
from sql_zugriff import *
print(generate_normal_hash("A5ENUZHR"))
print(execute_get_query("SELECT OTP FROM User WHERE UserID = 1")[0][0])
print(generate_normal_hash("A5ENUZHR") == execute_get_query("SELECT OTP FROM User WHERE UserID = 1")[0][0])"""