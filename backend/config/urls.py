
from django.contrib import admin
from django.urls import path, include # 記得 import include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 將所有 /api/ 開頭的網址，都交給 api 這個 app 的 urls.py 去處理
    path('api/', include('api.urls')),
]