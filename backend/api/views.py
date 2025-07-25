# backend/api/views.py

# 1. 清理並整理所有的 import
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Project, Profile
from .serializers import ProjectSerializer, UserSerializerWithToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer # 引入我們新的 Serializer
from rest_framework.permissions import IsAuthenticated # 引入 IsAuthenticated 權限
from .models import Application # 引入 Application 模型
from .serializers import ApplicationSerializer # 引入 ApplicationSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    def perform_create(self, serializer):
        # 當建立新的計畫時，自動將 owner 設為當前登入的使用者
        serializer.save(owner=self.request.user)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    """
    處理活動申請的 API。
    - 建立申請 (POST): 必須是已登入的使用者。
    - 查看申請 (GET): 未來可以設定權限，讓計畫主持人看到他收到的申請。
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated] # 設定權限：必須登入才能操作

    def perform_create(self, serializer):
        # 當建立新的申請時，自動將申請人(applicant)設定為當前登入的使用者
        serializer.save(applicant=self.request.user)