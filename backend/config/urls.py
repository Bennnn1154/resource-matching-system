from django.contrib import admin
from django.urls import path, include
# 移除舊的 TokenObtainPairView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView # 只保留 TokenRefreshView
from api.views import MyTokenObtainPairView # 引入我們自己的 View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # --- 將 token_obtain_pair 指向我們客製化的 View ---
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]