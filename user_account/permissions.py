from rest_framework.permissions import BasePermission



class IsProductCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.pk == obj.user.pk)
