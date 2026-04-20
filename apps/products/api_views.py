from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    formatted_price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'description',
                  'price', 'formatted_price', 'image', 'stock', 'is_featured']


class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(is_available=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class CategoryListAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
