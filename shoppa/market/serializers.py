from rest_framework import serializers

from .models import ShopOwner, Customer, Product, Cart, CartItem, Category, SubCategory, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    categoryinfo = CategorySerializer(source='category', read_only=True)
    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    #category = SubCategorySerializer(many=False, read_only=True)
    subcategory = SubCategorySerializer(source='category', read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        if instance.price <= 0:
            instance.price = 1

        instance.prod_desc = validated_data.get('prod_desc', instance.prod_desc)
        instance.img = validated_data.get('img', instance.img)
        #instance.category = validated_data.get('category', instance.category)
        #category = SubCategory.objects.get(pk=validated_data.get('category', instance.category))
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    
    def create(self, validated_data):
        return Cart.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.date = validated_data.get('name', instance.date)
        instance.sum_cost = validated_data.get('price', instance.sum_cost)
        instance.save()
        return instance

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='product_id', read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'
    
    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        if instance.quantity <= 0:
            instance.quantity = 1

        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        #instance.item_price = validated_data.get('item_price', instance.item_price)
        instance.item_price = instance.unit_price*instance.quantity
        
        instance.save()
        return instance
    
