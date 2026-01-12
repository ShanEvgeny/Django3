from rest_framework.permissions import BasePermission
                                  
class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.has_perm('general.can_read_objects') and
                    request.user.has_perm('general.can_create_objects') and
                    request.user.has_perm('general.can_update_objects') and
                    request.user.has_perm('general.can_delete_objects'))
                                     