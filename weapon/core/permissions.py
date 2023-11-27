from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "This user is not owner of this object."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsLectureOwnerOrReadOnly(permissions.BasePermission):
    message = "This user is not owner of this object."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.lecture.user == request.user

class HasProfileOrReadOnly(permissions.BasePermission):
    message = "This user doesn't have a profile."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return hasattr(request.user, "profile")

class IsPhoneNumberVerifiedOrReadOnly(permissions.BasePermission):
    message = "This user's phone number is not verified."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        pn = request.user.phonenumber
        if pn:
            return pn.is_verified
        return False
