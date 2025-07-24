from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import viewsets
from rest_framework import viewsets, generics # 引入 generics
from rest_framework.permissions import AllowAny # 引入 AllowAny
from .serializers import ProjectSerializer, UserSerializerWithToken # 引入 UserSerializerWithToken

@api_view(['GET']) # 表示這個視圖只接受 GET 請求

class RegisterView(generics.CreateAPIView):
    """
    一個只接受 POST 請求的視圖，用於建立新使用者。
    """
    queryset = User.objects.all()
    # 任何人都可以註冊，所以權限設為 AllowAny
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerWithToken

def hello_world(request):
    """
    一個簡單的 API 範例，回傳一個 JSON 物件。
    """
    return Response({"message": "Hello from Django Backend!"})


class ProjectViewSet(viewsets.ModelViewSet):
    """
    一個可以處理所有關於「計畫」的 API 視圖集。
    它會自動提供 list(列表), create(建立), retrieve(單一查詢),
    update(更新), destroy(刪除) 等操作。
    """
    queryset = Project.objects.all().order_by('-created_at') # 預設查詢所有計畫，並依建立時間排序
    serializer_class = ProjectSerializer