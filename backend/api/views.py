# backend/api/views.py

# 1. 清理並合併所有 import 語句，讓程式碼更乾淨
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Application, Project, Profile
from .serializers import (
    ApplicationSerializer, MyTokenObtainPairSerializer, ProjectSerializer,
    UserSerializerWithToken
)

# --------------------------------------------------------------------------

@api_view(['GET'])
def hello_world(request):
    """
    一個簡單的 API 範例，回傳一個 JSON 物件。
    """
    return Response({"message": "Hello from Django Backend!"})


class RegisterView(generics.CreateAPIView):
    """
    一個只接受 POST 請求的視圖，用於建立新使用者。
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerWithToken


class MyTokenObtainPairView(TokenObtainPairView):
    """
    使用我們客製化的 Serializer 來核發 Token。
    """
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    處理所有關於「計畫」的 API。
    """
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    
    # --- ✅ 核心修正點：新增這一行權限設定 ---
    # IsAuthenticatedOrReadOnly 的意思是：
    # - 對於安全的讀取操作 (GET)，任何人都可以訪問。
    # - 對於不安全的寫入操作 (POST, PUT, DELETE)，必須是已登入的使用者才能訪問。
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        # 因為上面的權限設定，能執行到這裡的 self.request.user 一定是已登入的使用者
        serializer.save(owner=self.request.user)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    處理活動申請的 API。
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)