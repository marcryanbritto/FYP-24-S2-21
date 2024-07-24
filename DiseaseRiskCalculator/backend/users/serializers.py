# serializers.py
from rest_framework import serializers
from .models import User, Gene, UserActivity, Formula

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active']
        read_only_fields = ['id']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class GeneSerializer(serializers.ModelSerializer):
    sequence = serializers.SerializerMethodField()

    class Meta:
        model = Gene
        fields = ['id', 'name', 'sequence', 'uploaded_by', 'date_added']
        read_only_fields = ['id', 'uploaded_by', 'date_added']

    def get_sequence(self, obj):
        return obj.decrypt_sequence()

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)

class GeneFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    name = serializers.CharField(max_length=255, required=False)
    sequence = serializers.CharField(required=False)
    
    def validate(self, data):
        file = data.get('file', None)
        if file:
            if not file.name.endswith('.txt'):
                raise serializers.ValidationError("Only .txt files are allowed.")
            content = file.read().decode('utf-8').strip()
            data['sequence'] = content
        return data

class GeneTextInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    sequence = serializers.CharField()

class UserActivitySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'user_email', 'action', 'timestamp']

class FormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formula
        fields = ['id', 'formula', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        # Ensure only one formula exists
        Formula.objects.all().delete()
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)