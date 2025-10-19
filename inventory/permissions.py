# inventory/permissions.py
from rest_framework import permissions

class IsBarManagerStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Superuser & BarManager: full CRUD
    - Staff: read all except ItemValue, can edit only 'sold'
    - Accountant: read-only
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Deny staff access to ItemValue views entirely
        if user.groups.filter(name='Staff').exists():
            if hasattr(view, 'queryset') and view.queryset.model.__name__ == 'ItemValue':
                return False

        # Allow read for all authenticated users except staff on ItemValue
        if request.method in permissions.SAFE_METHODS:
            return True

        # Superuser & BarManager full access
        if user.is_superuser or user.groups.filter(name='BarManager').exists():
            return True

        # Staff can write (but restricted later)
        if user.groups.filter(name='Staff').exists():
            return True

        # Accountant read-only
        if user.groups.filter(name='Accountant').exists():
            return False

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Superuser & BarManager full access
        if user.is_superuser or user.groups.filter(name='BarManager').exists():
            return True

        # Block staff from ItemValue at object level too
        if user.groups.filter(name='Staff').exists():
            if obj.__class__.__name__ == 'ItemValue':
                return False

            if request.method in ['PUT', 'PATCH']:
                allowed_fields = getattr(
                    getattr(view.serializer_class, 'Meta', None),
                    'staff_editable_fields',
                    []
                )
                return set(request.data.keys()).issubset(allowed_fields)

            return request.method in permissions.SAFE_METHODS

        # Accountant read-only
        if user.groups.filter(name='Accountant').exists():
            return request.method in permissions.SAFE_METHODS

        return False
