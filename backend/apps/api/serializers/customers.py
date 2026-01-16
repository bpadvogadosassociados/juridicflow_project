from rest_framework import serializers
from apps.customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer completo de Customer.
    """
    document_formatted = serializers.ReadOnlyField()
    total_processes = serializers.ReadOnlyField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'organization',
            'office',
            'name',
            'type',
            'type_display',
            'document',
            'document_formatted',
            'email',
            'phone',
            'phone_secondary',
            'address',
            'city',
            'state',
            'zip_code',
            'notes',
            'is_active',
            'total_processes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization', 'office']
    
    def create(self, validated_data):
        """
        Injeta organization e office do request automaticamente.
        """
        request = self.context.get('request')
        validated_data['organization'] = request.organization
        validated_data['office'] = request.office
        return super().create(validated_data)


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem (performance).
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'type',
            'type_display',
            'document',
            'email',
            'phone',
            'is_active',
            'created_at'
        ]


class CustomerCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação/edição (sem campos read-only).
    """
    class Meta:
        model = Customer
        fields = [
            'name',
            'type',
            'document',
            'email',
            'phone',
            'phone_secondary',
            'address',
            'city',
            'state',
            'zip_code',
            'notes',
            'is_active'
        ]