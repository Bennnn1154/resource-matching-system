from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 引入我們的新視圖 RegisterView
from .views import hello_world, ProjectViewSet, RegisterView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('hello/', hello_world, name='hello-world'),
    # --- 以下是我們為註冊新增的路由 ---
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]