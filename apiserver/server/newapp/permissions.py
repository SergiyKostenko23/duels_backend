from rest_framework.permissions import BasePermission, SAFE_METHODS

from .views import User

#Permissões de users
class CreateUserPermssion(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.filter(email=request.user)
        metodo = request.method
        if metodo != SAFE_METHODS and user[0].tipo_user == "superuser":
            return True
        elif metodo == SAFE_METHODS:
            return True
        else:
            return False

class GetPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == SAFE_METHODS:
            return True
        else:
            return False