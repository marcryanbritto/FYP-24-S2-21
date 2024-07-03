# Take model (Account) and translate into JSON
from .models import Account

from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'username', 'password', 'role',
                  'isDeactivated', 'email', 'registrationDate')

# Takes data that needs to be sent to POST
class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'username', 'password', 'role', 'email')
        