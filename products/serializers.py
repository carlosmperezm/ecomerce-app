"""Product app Serializers"""

from rest_framework.serializers import ModelSerializer

from products.models import Category, Product


class CategorySerializer(ModelSerializer):
    """Serializer for each categories"""

    class Meta:
        """create the class fields automatically"""

        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    """Product for each categories"""

    category: CategorySerializer = CategorySerializer(required=False)

    class Meta:
        """Create the class fields automatically"""

        model = Product
        fields = "__all__"
