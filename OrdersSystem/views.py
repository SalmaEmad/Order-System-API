import os, json
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, views,viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import ProductForm


class CustomTokenObtainPairView(TokenObtainPairView):
   def post(self, request, *args, **kwargs):
      try:
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        response.data['name'] =  user.first_name + " " + user.last_name
        if user.is_superuser:
            response.data['role'] = "Admin"
        else:
            response.data['role'] = "User"
        return Response({'code': status.HTTP_200_OK, 'message': "Success", 'data': response.data})
      except Exception as e:
        return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': "Failed", 'data': str(e)})


@api_view(['GET'])
def GetProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({'code': status.HTTP_200_OK, 'message': serializer.data})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def CreateProduct(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return Response({'code': status.HTTP_200_OK, 'message': ""})
    return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': form.errors.as_json()})

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def ModifyProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'code': status.HTTP_404_NOT_FOUND, 'message': "The product does not exist"})
    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'code': status.HTTP_200_OK, 'message': serializer.data})
    return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': serializer.errors})

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def DeleteProduct(request, pk):
    product = Product.objects.get(pk=pk)
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'code': status.HTTP_404_NOT_FOUND, 'message': "The product does not exist"})
    product.delete()
    return Response({'code': status.HTTP_200_OK, 'message': "Product deleted successfully"})

@api_view(['PUT'])
def PurchaseProduct(request, pk):
    if not request.user.is_superuser:
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'code': status.HTTP_404_NOT_FOUND, 'message': "The product does not exist"})
        currentUser = User.objects.get(pk=request.user.pk)
        try:
            newPurchase = product.Users.add(request.user.pk)
        except:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': "The purchasement process failed"})
        return Response({'code': status.HTTP_200_OK, 'message':'You purchased the product successfully'})

@api_view(['GET'])
def GetPurchasedProducts(request):
    if not request.user.is_superuser:
        products = Product.objects.filter(Users = request.user)
        serializer = ProductSerializer(products, many=True)
        return Response({'code': status.HTTP_200_OK, 'message': serializer.data})