# inventory/permissions.py
from rest_framework import permissions

class IsBarManagerStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Superuser & BarManager: full CRUD
    - Staff: read all, can edit only 'sold'
    - Accountant: read-only
    """

    def has_permission(self, request, view):
        # Allow read for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Superusers & BarManagers can write
        if request.user.is_superuser or request.user.groups.filter(name='BarManager').exists():
            return True

        # Staff can write, but limited at object level
        if request.user.groups.filter(name='Staff').exists():
            return True

        # Accountant cannot write
        if request.user.groups.filter(name='Accountant').exists():
            return False

        return False

    def has_object_permission(self, request, view, obj):
        # Superuser & BarManager can do anything
        if request.user.is_superuser or request.user.groups.filter(name='BarManager').exists():
            return True

        # Staff can only edit allowed fields
        if request.user.groups.filter(name='Staff').exists():
            if request.method in ['PUT', 'PATCH']:
                allowed_fields = getattr(
                    getattr(view.serializer_class, 'Meta', None),
                    'staff_editable_fields',
                    []
                )
                return set(request.data.keys()).issubset(allowed_fields)
            return request.method in permissions.SAFE_METHODS

        # Accountant: read-only
        if request.user.groups.filter(name='Accountant').exists():
            return request.method in permissions.SAFE_METHODS

        return False
