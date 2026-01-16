from rest_framework import serializers
from apps.processes.models import Process, ProcessParty
from apps.api.serializers.customers import CustomerListSerializer

class ProcessPartySerializer(serializers.ModelSerializer):
    """
    Serializer para partes do processo.
    """
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = ProcessParty
        fields = [
            'id',
            'customer',
            'customer_name',
            'role',
            'role_display',
            'notes',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProcessSerializer(serializers.ModelSerializer):
    """
    Serializer completo de Process (com partes inline).
    """
    parties = ProcessPartySerializer(many=True, read_only=True)
    area_display = serializers.CharField(source='get_area_display', read_only=True)
    phase_display = serializers.CharField(source='get_phase_display', read_only=True)
    parties_count = serializers.ReadOnlyField()
    deadlines_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Process
        fields = [
            'id',
            'organization',
            'office',
            'number',
            'internal_number',
            'area',
            'area_display',
            'subject',
            'court',
            'court_division',
            'phase',
            'phase_display',
            'value',
            'distribution_date',
            'notes',
            'is_active',
            'is_confidential',
            'parties',
            'parties_count',
            'deadlines_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization', 'office']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['organization'] = request.organization
        validated_data['office'] = request.office
        return super().create(validated_data)


class ProcessListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem.
    """
    area_display = serializers.CharField(source='get_area_display', read_only=True)
    phase_display = serializers.CharField(source='get_phase_display', read_only=True)
    parties_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Process
        fields = [
            'id',
            'number',
            'subject',
            'area',
            'area_display',
            'phase',
            'phase_display',
            'court',
            'parties_count',
            'is_active',
            'created_at'
        ]


class ProcessCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação/edição.
    """
    parties = ProcessPartySerializer(many=True, required=False)
    
    class Meta:
        model = Process
        fields = [
            'number',
            'internal_number',
            'area',
            'subject',
            'court',
            'court_division',
            'phase',
            'value',
            'distribution_date',
            'notes',
            'is_active',
            'is_confidential',
            'parties'
        ]
    
    def create(self, validated_data):
        parties_data = validated_data.pop('parties', [])
        
        request = self.context.get('request')
        validated_data['organization'] = request.organization
        validated_data['office'] = request.office
        
        process = Process.objects.create(**validated_data)
        
        # Criar partes
        for party_data in parties_data:
            ProcessParty.objects.create(process=process, **party_data)
        
        return process
    
    def update(self, instance, validated_data):
        parties_data = validated_data.pop('parties', None)
        
        # Atualizar processo
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualizar partes (se fornecidas)
        if parties_data is not None:
            # Remove partes antigas
            instance.parties.all().delete()
            # Cria novas
            for party_data in parties_data:
                ProcessParty.objects.create(process=instance, **party_data)
        
        return instance