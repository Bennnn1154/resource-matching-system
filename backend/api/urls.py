from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import hello_world, ProjectViewSet # 引入 ProjectViewSet

# 建立一個 router 物件
router = DefaultRouter()
# 註冊我們的 ProjectViewSet，DRF 會自動為它產生一組 URL
# 'projects' 是我們希望在 URL 中看到的名稱，例如 /api/projects/
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('hello/', hello_world, name='hello-world'),
    # 將 router 產生的 URL 全部包含進來
    path('', include(router.urls)),
]