from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class IsDoctorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_doctor or request.user.is_staff


class IsPatientOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_patient or request.user.is_staff


class IsResultForPatient(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_patient

    def has_object_permission(self, request, view, obj):
        return request.user.is_patient and request.user.email == obj.target_patient.email
