from graphene_django import DjangoObjectType
import graphene
from graphene import AbstractType, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from data_api.models import UnitOfMeasureCategory, UnitOfMeasure, Dimension, Product, Coord, TimeWindow, OrderItem, InventoryItem, Location, CarrierClass, Carrier, Customer, Order, MapOutWay, MapWay, Map, Trip

from graphene_django.debug import DjangoDebug

class UnitOfMeasureCategoryNode(DjangoObjectType):
    class Meta:
        model = UnitOfMeasureCategory
        interfaces = (Node, )
        filter_fields = ['name', ]

class UnitOfMeasureNode(DjangoObjectType):
    class Meta:
        model = UnitOfMeasure
        interfaces = (Node, )
        filter_fields = ['name', ]

class Query(AbstractType, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

    uom_category = Node.Field(UnitOfMeasureCategoryNode)
    all_uom_categories = DjangoFilterConnectionField(UnitOfMeasureCategoryNode)

    uom = Node.Field(UnitOfMeasureNode)
    all_uom = DjangoFilterConnectionField(UnitOfMeasureNode)

schema = graphene.Schema(query=Query)
