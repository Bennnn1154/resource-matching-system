from django.contrib import admin
from django.urls import path, include
# 從 simplejwt.views 引入需要的視圖
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # --- 以下是我們為 JWT 新增的路由 ---
    # 使用者可以訪問 /api/token/ 來獲取 access 和 refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 使用者可以訪問 /api/token/refresh/ 來用 refresh token 換取新的 access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]