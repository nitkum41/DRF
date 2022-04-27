from .permissions import IsStaffEditorPermission
from rest_framework import permissions

#it can be used by any view class that requires permissions

#it can be used for permissions, queryset, serializser classes
class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]



# associate ownership of data...so superuser cannot see data created by staff
class UserQuerySetMixin():
    user_field='user'     # it could be owner
    allow_staff_view = False
    def get_queryset(self,*args,**kwargs):
        user = self.request.user
        lookup_data={}
        lookup_data[self.user_field]=user
        qs = super().get_queryset(*args,**kwargs) #default queryset
        if user.is_staff and self.allow_staff_view:
            return qs
        
        return qs.filter(**lookup_data)  #self.user_field=self.request.user as filter
