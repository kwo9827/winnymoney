from .models import DepositOptions, DepositProducts 
from rest_framework import serializers

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

class TopRateSerializer(serializers.ModelSerializer):
    deposit_product = DepositProductsSerializer(source='product', read_only=True)

    class Meta:
        model = DepositOptions
        fields = '__all__'
