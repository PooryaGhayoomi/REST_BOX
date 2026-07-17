from rest_framework.permissions import BasePermission


class IsVillaOwnerHost(BasePermission):
    """
    فقط hostِ مالکِ همان ویلا اجازه دارد تقویم (Availability) آن را تغییر دهد.
    بررسی مالکیت داخل view روی شیء villa انجام می‌شود، این کلاس فقط
    احراز هویت اولیه و نقش HOST را چک می‌کند.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "HOST"
        )
