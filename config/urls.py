from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import status, routers
from rest_framework.authtoken.views import obtain_auth_token

from weapon.accounts.views import PhoneNumberViewSet, ProfileViewSet, CustomUserDetailsView, KakaoLoginView, \
    RequestDeleteUserViewSet, RecommendCodeView
from weapon.contacts.views import SuggestViewSet
from weapon.customers.views import CustomerViewSet, CustomerMedicalHistoryViewSet
from weapon.insurances.views import CommonInsuranceApiViewSet, CustomerInsuranceViewSet
from weapon.membership.views import MembershipViewSet, PaymentViewSet, UserMembershipViewSet

router = routers.SimpleRouter()
router.register(r'accounts/phonenumber', PhoneNumberViewSet, basename="phonenumber")
router.register(r'accounts/request_delete_user', RequestDeleteUserViewSet, basename="request_delete_user")
router.register(r'accounts/profile', ProfileViewSet, basename="profile")
router.register(r'contact/suggest', SuggestViewSet, basename="contact_suggest")
router.register(r'customer', CustomerViewSet, basename="customer")
router.register(r'customer_insurance', CustomerInsuranceViewSet, basename="customer_insurance")
router.register(r'customer_medical_history', CustomerMedicalHistoryViewSet, basename="customer_medical_history")
router.register(r'membership', MembershipViewSet, basename="membership")
router.register(r'user_membership', UserMembershipViewSet, basename="user_membership")
router.register(r'payment', PaymentViewSet, basename="payment")

rest_auth_urlpatterns = [
    # URLs that do not require a session or valid token
    # url(r'^password/reset/$', PasswordResetView.as_view(),
    #     name='rest_password_reset'),
    # url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
    #     name='rest_password_reset_confirm'),
    # url(r'^login/$', INENVocaLoginView.as_view(), name='rest_login'),
    url(r'^kakao_login/$', KakaoLoginView.as_view(), name='kakao_login'),
    # URLs that require a user to be logged in with a valid session / token.
    # url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', CustomUserDetailsView.as_view(), name='rest_user_details'),
    # url(r'^password/change/$', PasswordChangeView.as_view(),
    #     name='rest_password_change'),ㅋ
]

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("weapon.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    # summer note
    path('api/v1/user/', CustomUserDetailsView.as_view()),
    path('api/v1/common/insurance/', CommonInsuranceApiViewSet.as_view()),
    path('api/v1/recommend_code/', RecommendCodeView.as_view()),

    # path('api/v1/phone_number_login/', CreatePhoneNumberUser.as_view()),
    path('summernote/', include('django_summernote.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    path('api/v1/', include(router.urls)),
    path('api/v1/rest-auth/', include(rest_auth_urlpatterns)),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
