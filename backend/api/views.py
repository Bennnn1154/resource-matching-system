from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import viewsets

@api_view(['GET']) # 表示這個視圖只接受 GET 請求
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