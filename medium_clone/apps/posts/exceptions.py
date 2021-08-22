from rest_framework.exceptions import APIException


class UserNoAccount(APIException):
    status_code = 400
    default_detail = "User doesn't have a account."
    default_code = "user_no_account"
