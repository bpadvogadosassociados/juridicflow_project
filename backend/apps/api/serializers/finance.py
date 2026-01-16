from rest_framework import serializers
from apps.finance.models import FeeAgreement, Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer de Payment.
    """
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'organization',
            'office',
            'fee_agreement',
            'description',
            'amount',
            'due_date',
            'payment_date',
            'payment_method',
            'payment_method_display',
            'status',
            'status_display',
            'receipt_file',
            'notes',
            'is_overdue',
            'days_overdue',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization', 'office']


class FeeAgreementSerializer(serializers.ModelSerializer):
    """
    Serializer completo de FeeAgreement.
    """
    payments = PaymentSerializer(many=True, read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    process_number = serializers.CharField(source='process.number', read_only=True)
    total_received = serializers.ReadOnlyField()
    total_pending = serializers.ReadOnlyField()
    percentage_received = serializers.ReadOnlyField()
    is_fully_paid = serializers.ReadOnlyField()
    
    class Meta:
        model = FeeAgreement
        fields = [
            'id',
            'organization',
            'office',
            'customer',
            'customer_name',
            'process',
            'process_number',
            'title',
            'type',
            'type_display',
            'description',
            'amount',
            'success_percentage',
            'hourly_rate',
            'installments',
            'installment_amount',
            'start_date',
            'end_date',
            'status',
            'status_display',
            'notes',
            'contract_file',
            'payments',
            'total_received',
            'total_pending',
            'percentage_received',
            'is_fully_paid',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organization', 'office', 'installment_amount']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['organization'] = request.organization
        validated_data['office'] = request.office
        return super().create(validated_data)


class FeeAgreementListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem.
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    percentage_received = serializers.ReadOnlyField()
    
    class Meta:
        model = FeeAgreement
        fields = [
            'id',
            'customer_name',
            'title',
            'type',
            'type_display',
            'amount',
            'status',
            'status_display',
            'percentage_received',
            'start_date',
            'created_at'
        ]