
from django.db import migrations

def set_is_staff(apps, schema_editor):
    User = apps.get_model('users', 'User')
    for user in User.objects.all():
        if user.role == "admin" or user.role == "Admin":
        # Set is_staff to True or False as needed
            user.is_staff = True  # or False
            user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20240808_1455'),  # Replace with the actual last migration file in the users app
    ]

    operations = [
        migrations.RunPython(set_is_staff),
    ]
