from rest_framework import serializers
from apps.documents.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer completo de Document.
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    file_extension = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    file_icon = serializers.ReadOnlyField()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'organization',
            'office',
            'title',
            'category',
            'category_display',
            'description',
            'file',
            'file_url',
            'file_size',
            'file_extension',
            'file_size_mb',
            'file_icon',
            'content_type',
            'object_id',
            'uploaded_by',
            'uploaded_by_name',
            'is_confidential',
            'version',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization', 'office', 'uploaded_by', 'file_size']
    
    def get_file_url(self, obj):
        """Retorna URL completa do arquivo"""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['organization'] = request.organization
        validated_data['office'] = request.office
        validated_data['uploaded_by'] = request.user
        return super().create(validated_data)


class DocumentListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem.
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    file_extension = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'category',
            'category_display',
            'file_extension',
            'file_size_mb',
            'is_confidential',
            'created_at'
        ]


class DocumentUploadSerializer(serializers.ModelSerializer):
    """
    Serializer para upload de documento.
    """
    class Meta:
        model = Document
        fields = [
            'title',
            'category',
            'description',
            'file',
            'content_type',
            'object_id',
            'is_confidential',
            'notes'
        ]