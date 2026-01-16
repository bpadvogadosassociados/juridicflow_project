from rest_framework import serializers
from apps.accounts.models import User
from apps.memberships.models import Membership

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer básico de usuário.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'is_active',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.email


class MembershipSerializer(serializers.ModelSerializer):
    """
    Serializer de membership (com organização e office).
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    office_name = serializers.CharField(source='office.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = Membership
        fields = [
            'id',
            'organization',
            'organization_name',
            'office',
            'office_name',
            'role',
            'role_display',
            'is_active'
        ]


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer para resposta de login.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
    memberships = MembershipSerializer(many=True)