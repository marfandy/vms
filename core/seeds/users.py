from authentication.models import Account


def seeding_user(apps, schema_editor):
    user = Account()
    user.first_name = "Admin"
    user.username = "admin"
    user.set_password("admin!@#")
    user.save()
