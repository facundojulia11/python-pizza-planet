from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column, func, extract

from .models import Ingredient, Beverage, Order, OrderDetail, Size, db
from .serializers import (IngredientSerializer, BeverageSerializer, OrderSerializer,
                          SizeSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
    
class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id)
                             for ingredient in ingredients))
        if beverages:
            cls.session.add_all(
            OrderDetail(order_id=new_order._id, beverage_id=beverage._id)
            for beverage in beverages
        )
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')

class ReportManager():
    session = db.session
    serializer = IngredientSerializer

    @classmethod
    def get_report(cls):
        data = {
            "most_requested_ingredient":cls.get_most_requested_ingredient(cls),
            "most_revenue_month": cls.get_month_with_highest_revenue(cls),
            "top_three_customers": cls.get_top_customers(cls)
        }
        return data


    def get_most_requested_ingredient(cls):

        most_requested = (
            cls.session.query(OrderDetail.ingredient_id, func.count(OrderDetail.ingredient_id).label('ingredient_count'))
            .group_by(OrderDetail.ingredient_id)
            .order_by(func.count(OrderDetail.ingredient_id).desc())
            .first()
        )

        if not most_requested:
            return None

        ingredient = cls.session.query(Ingredient).get(most_requested.ingredient_id)
        
        most_requested_ingredient={
            "ingredient": ingredient.name,
            "count": most_requested.ingredient_count
        }

        return most_requested_ingredient
    
    def get_month_with_highest_revenue(cls):
        revenue_by_month = (
            cls.session.query(
                extract('year', Order.date).label('year'),
                extract('month', Order.date).label('month'),
                func.sum(Order.total_price).label('total_revenue')
            )
            .group_by('year', 'month')
            .order_by(func.sum(Order.total_price).desc())
            .first()
        )

        if not revenue_by_month:
            return None

        most_revenue_month={
            "month": revenue_by_month.month,
            "year": revenue_by_month.year,
            "total": revenue_by_month.total_revenue,
        }

        return most_revenue_month
    
    def get_top_customers(cls):
        top_customers = (
            cls.session.query(
                Order.client_name,
                func.count(Order._id).label('order_count')
            )
            .group_by(Order.client_name)
            .order_by(func.count(Order._id).desc())
            .limit(3)
            .all()
        )
        
        result = [{"client_name": customer.client_name, "order_count": customer.order_count} for customer in top_customers]

        return result




class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()
