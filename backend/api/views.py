# backend/api/views.py

# 1. 清理並整理所有的 import
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Project, Profile
from .serializers import ProjectSerializer, UserSerializerWithToken

# 2. 將裝飾器放回 hello_world 函式的正上方
@api_view(['GET'])
def hello_world(request):
    """
    一個簡單的 API 範例，回傳一個 JSON 物件。
    """
    return Response({"message": "Hello from Django Backend!"})

# 3. 保持每個 Class 和 Function 的獨立與完整
class RegisterView(generics.CreateAPIView):
    """
    一個只接受 POST 請求的視圖，用於建立新使用者。
    """
    queryset = User.objects.all()
    # 任何人都可以註冊，所以權限設為 AllowAny
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerWithToken

class ProjectViewSet(viewsets.ModelViewSet):
    """
    一個可以處理所有關於「計畫」的 API 視圖集。
    它會自動提供 list(列表), create(建立), retrieve(單一查詢),
    update(更新), destroy(刪除) 等操作。
    """
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer