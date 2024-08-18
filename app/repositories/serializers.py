from app.plugins import ma
from .models import Ingredient, Beverage, Size, Order, OrderDetail


class BaseSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        fields = ('_id', 'name', 'price')


class IngredientSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Ingredient

class SizeSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Size

class BeverageSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Beverage


class OrderDetailSerializer(ma.SQLAlchemyAutoSchema):

    ingredient = ma.Nested(IngredientSerializer)
    beverage = ma.Nested(BeverageSerializer)

    class Meta:
        model = OrderDetail
        load_instance = True
        fields = (
            'ingredient_price',
            'ingredient',
            'beverage_price',
            'beverage'
        )


class OrderSerializer(ma.SQLAlchemyAutoSchema):
    size = ma.Nested(SizeSerializer)
    detail = ma.Nested(OrderDetailSerializer, many=True)

    class Meta:
        model = Order
        load_instance = True
        fields = (
            '_id',
            'client_name',
            'client_dni',
            'client_address',
            'client_phone',
            'date',
            'total_price',
            'size',
            'detail'
        )
