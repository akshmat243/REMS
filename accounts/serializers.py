from rest_framework import serializers
from MBP.models import Role
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.role = None 
        user.created_by = None
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    
    role = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Role.objects.all()
    )
    
    password = serializers.CharField(write_only=True, required=False)
    role_slug = serializers.SlugField(write_only=True, required=False)
    role = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'slug', 'password',
            'role_slug', 'role', 'is_active', 'date_joined', 'created_by'
        ]
        read_only_fields = ['id', 'date_joined', 'created_by', 'role']

    def get_role(self, obj):
        return obj.role.name if obj.role else None

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        role_slug = validated_data.pop('role_slug', None)

        role = None
        if role_slug:
            try:
                role = Role.objects.get(slug=role_slug)
            except Role.DoesNotExist:
                raise serializers.ValidationError({"role_slug": "Invalid role slug."})

        user = User(**validated_data)
        if password:
            user.set_password(password)
        if role:
            user.role = role
        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        role_slug = validated_data.pop('role_slug', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        if role_slug:
            try:
                role = Role.objects.get(slug=role_slug)
                instance.role = role
            except Role.DoesNotExist:
                raise serializers.ValidationError({"role_slug": "Invalid role slug."})

        instance.save()
        return instance
