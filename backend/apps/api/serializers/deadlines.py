from rest_framework import serializers
from apps.deadlines.models import Deadline

class DeadlineSerializer(serializers.ModelSerializer):
    """
    Serializer completo de Deadline.
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    responsible_name = serializers.CharField(source='responsible.get_full_name', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Deadline
        fields = [
            'id',
            'organization',
            'office',
            'title',
            'description',
            'type',
            'type_display',
            'due_date',
            'due_time',
            'completed_at',
            'priority',
            'priority_display',
            'status',
            'status_display',
            'responsible',
            'responsible_name',
            'content_type',
            'object_id',
            'alert_days_before',
            'alert_sent',
            'notes',
            'is_overdue',
            'days_remaining',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization', 'office', 'completed_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['organization'] = request.organization
        validated_data['office'] = request.office
        return super().create(validated_data)


class DeadlineListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem.
    """
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Deadline
        fields = [
            'id',
            'title',
            'due_date',
            'due_time',
            'priority',
            'priority_display',
            'status',
            'status_display',
            'is_overdue',
            'days_remaining',
            'created_at'
        ]


class DeadlineCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação/edição.
    """
    class Meta:
        model = Deadline
        fields = [
            'title',
            'description',
            'type',
            'due_date',
            'due_time',
            'priority',
            'status',
            'responsible',
            'content_type',
            'object_id',
            'alert_days_before',
            'notes'
        ]