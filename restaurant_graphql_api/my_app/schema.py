import graphene
from graphene_django import DjangoObjectType
from .models import Restaurant

class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant
        fields = ('id','name','address')



class Query(graphene.ObjectType):
    """
    queries for the restaurant model
    """
    restaurants = graphene.List(RestaurantType)

    def resolve_restaurants(self,info, **kwargs):
        return Restaurant.objects.all()
    
schema = graphene.Schema(query=Query)

#create restaurant 
class CreateRestaurant(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        address = graphene.String()
    
    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)
    
    def mutate(self,info,name,address):
        restaurant = Restaurant(name,address)
        restaurant.save()
        return CreateRestaurant(ok=True,restaurant=restaurant)
    
#delete restaurant
class DeleteRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
    
    ok = graphene.Boolean()
    
    def mutate(self,info,id):
        restaurant = Restaurant.objects.get(id=id)
        restaurant.delete()
        return DeleteRestaurant(ok=True)

#update the restaurant
class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        address = graphene.String()

    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)

    def mutate(self,info,id,name,address):
        restaurant = Restaurant.objects.get(id=id)
        restaurant.name = name
        restaurant.address = address
        restaurant.save()
        return UpdateRestaurant(ok=True,restaurant=restaurant)
    

class Mutation(graphene.ObjectType):
    create_restaurant = CreateRestaurant.Field()
    delete_restaurant = DeleteRestaurant.Field()
    update_restaurant = UpdateRestaurant.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)