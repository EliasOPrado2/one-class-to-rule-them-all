from rest_framework import serializers

# Template class for serializing
# serializer.py
class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

#viewsets.py
class GenericAPIView(generics.ListAPIView):
    def dispatch(self, request, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.queryset = self.model.objects.all()
        serializer = GeneralSerializer
        serializer.Meta.model = self.model
        self.serializer_class = serializer
        return super().dispatch(request, *args, **kwargs)
        
        
# To conclude this generator we need to create an URL route for each model in urls.py:
# urls.py
app = apps.get_app_config('testapp')

for model_name, model in app.models.items(): # <---- model added here
    urlpatterns.append(path(model_name, views.GenericAPIView.as_view(), {'model': model})) #< ---- model added here from loop.
    
    
    """
    
    Other approach.
    """
    
#You can create a generalized class for your view then pass the model and any other info through extra url paramaters.
#For example:

class URLModelAPIView(generics.ListAPIView):
    def dispatch(self, request, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.queryset = self.model.objects.all()
        self.serializer = kwargs.pop('serializer')
        return super().dispatch(request, *args, **kwargs)
    
# Then in your urls.py

from django.urls import path
from . import models, serializers, views

urlpatterns = [
    path(
        'customer/',
        views.URLModelAPIView.as_view(),
        {
            'model': models.Customer,
            'serializer': serializers.CustomerSerializer,
        }
    ),
    path(
        'customer_contact/',
        views.URLModelAPIView.as_view(),
        {
            'model': models.CustomerContact,
            'serializer': serializers.CustomerContactSerializer,
        }
    ),
]
# The same logic applies for viewsets when using a router.
