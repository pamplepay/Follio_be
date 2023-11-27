from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LinkVerificationThrottle(AnonRateThrottle):
    scope = 'linkverfication'


# class PaymentThrottle(UserRateThrottle):
#     scope = 'payment'
