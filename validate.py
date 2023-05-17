import re
from database import get_resourse , get_table
from boto3.dynamodb.conditions import Attr
# dynamodb = get_resourse()
# table = get_table()
def validate_username(username):
    # Username must contain only alphanumeric characters or underscores
    # and must not contain any spaces
    pattern = re.compile(r'^\w+$')
    return bool(pattern.match(username))

def validate_email(email):
    # Email must be a valid email address
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))

# def is_valid_username(username,table):
#     response = table.scan(FilterExpression=Attr('username').eq(username))
#     return len(response['Items']) == 0
