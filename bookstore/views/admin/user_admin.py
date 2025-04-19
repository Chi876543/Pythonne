from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ...models import User



class UserAdmin(BaseUserAdmin):
    # Các trường hiển thị trong danh sách người dùng
    list_display = ('username', 'email', 'full_name', 'role', 'status', 'is_staff', 'is_superuser')
    list_filter = ('role', 'status', 'is_staff', 'is_superuser')
    
    # Các trường hiển thị khi chỉnh sửa người dùng
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'status', 'groups')}),
    )
    
    # Các trường khi tạo người dùng mới
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'full_name', 'email', 'role', 'status', 'groups'),
        }),
    )
    
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)
    filter_horizontal = ()