from rest_framework.throttling import UserRateThrottle


class PhoneNumberSendRateThrottle(UserRateThrottle):
    scope = 'phone_number'
    rate = '3/m'
