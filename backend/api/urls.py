from django.urls import path, include
from rest_framework.routers import DefaultRouter
# 引入我們的新視圖 RegisterView
from .views import hello_world, ProjectViewSet, RegisterView, ApplicationViewSet # 引入 ApplicationViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'applications', ApplicationViewSet) # <-- 新增這一行來註冊 application 的 API

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # ... 其他 path ...
    path('', include(router.urls)),
]