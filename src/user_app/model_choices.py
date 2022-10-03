class UserAccountChoice:
    admin = "Administrator"
    staff = "Staff"
    user = "User"

    TYPE_CHOICES = (
        (admin, admin),
        (staff, staff),
        (user, user)
    )