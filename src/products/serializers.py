from rest_framework import serializers
from .models import Product, Category, ProductAttachment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = "__all__"
        exclude = ['created', 'modified',]



class GetProductsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['created', 'modified', 'quantity', 'merchant',]
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        representation['average_rating'] = instance.average_rating
        if instance.sale_percent:
            representation['sale_percent'] = str(int(instance.sale_percent)) + '%'


        if not instance.image or instance.image == 'null':
            representation['image'] = '../utils/black.jpg'
            # representation['image'] = None

        
        if not instance.on_sale or instance.on_sale == 'null':
            representation['on_sale'] = False
        
        if not instance.on_sale:
            del representation['sale_percent']
            del representation['price_after_sale']

        if instance.merchant:
            representation['merchant'] = {
                "merchant_name": instance.merchant.full_name,
                "phone": instance.merchant.phone_number,
                "address": instance.merchant.address,
            }

        return representation
    


class RetrieveProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['created', 'modified', 'quantity', 'merchant',]
        depth = 2

    def to_representation(self, instance):

        product_attachments = []
# 
        for attachment in ProductAttachment.objects.filter(product=instance):
            product_attachments.append(attachment)

        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }

        if not instance.on_sale:
            del representation['sale_percent']
            del representation['price_after_sale']

        if not instance.on_sale or instance.on_sale == 'null':
            representation['on_sale'] = False

        if instance.sale_percent:
            representation['sale_percent'] = str(int(instance.sale_percent)) + '%'
        representation['images'] = list(product_attachments)

        representation['average_rating'] = instance.average_rating
        representation['reviews'] = instance.get_reviews()

        if instance.merchant:
            representation['merchant'] = {
                "merchant_name": instance.merchant.full_name,
                "phone": instance.merchant.phone_number,
                "address": instance.merchant.address,
            } 

        return representation
    


class GetProductsSerializerForMerchants(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['created', 'modified', 'quantity', 'merchant',]
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        representation['average_rating'] = instance.average_rating

        if instance.sale_percent:
            representation['sale_percent'] = str(int(instance.sale_percent)) + '%'
        
        
        return representation
    


class RetrieveProductsSerializerForMerchants(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['created', 'modified', 'quantity', 'merchant',]
        depth = 2

    def to_representation(self, instance):

        product_attachments = []
# 
        for attachment in ProductAttachment.objects.filter(product=instance):
            product_attachments.append(attachment.get_attachment_url())

        representation = super().to_representation(instance)
        representation['category'] = {
            "id": instance.category.id,
            "name": instance.category.name
        }
        if instance.sale_percent:
            representation['sale_percent'] = str(int(instance.sale_percent)) + '%'
        representation['images'] = list(product_attachments)

        representation['average_rating'] = instance.average_rating
        representation['reviews'] = instance.get_reviews()

        return representation


    # handle multiple images upload
    def create(self, validated_data):
        print(validated_data)
        images_data = self.context.get('view').request.FILES
        print(images_data)
        product = Product.objects.create(**validated_data)
        for image_data in images_data.values():
            ProductAttachment.objects.create(product=product, attachment=image_data)
        return product
