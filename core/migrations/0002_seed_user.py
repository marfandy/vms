from django.db import migrations

from core.seeds.users import seeding_user


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seeding_user),
    ]
