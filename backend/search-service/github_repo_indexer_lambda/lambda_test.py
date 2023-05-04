from urllib import response
from lambda_function import lambda_handler

event = {}
context = None

response =  lambda_handler(event, context)
print(response)