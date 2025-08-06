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
from rest_framework.views import APIView
from rest_framework import status
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

class DashboardView(APIView):
    permission_classes = [IsAuthenticated] # 門禁設定：必須登入才能訪問

    def get(self, request, *args, **kwargs):
        # 檢查使用者身分是否為大學端
        if request.user.profile.user_type != 'university':
            return Response(
                {"detail": "您沒有權限訪問此頁面。"}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # 查詢只屬於當前登入使用者的所有計畫
        projects = Project.objects.filter(owner=request.user).order_by('-created_at')
        
        # 使用我們現有的 Serializer 來序列化資料
        project_serializer = ProjectSerializer(projects, many=True)
        
        # 我們可以進一步處理資料，將申請的詳細資料也包含進去
        dashboard_data = []
        for project_data in project_serializer.data:
            project_id = project_data['id']
            # 查詢每個計畫對應的申請
            applications = Application.objects.filter(project_id=project_id)
            application_serializer = ApplicationSerializer(applications, many=True)
            # 將申請資料加入到計畫資料中
            project_data['applications_details'] = application_serializer.data
            dashboard_data.append(project_data)

        return Response(dashboard_data)