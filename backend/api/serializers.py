from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Project # 引入 Profile
from rest_framework_simplejwt.tokens import RefreshToken

# ... 您原有的 ProjectSerializer ...
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# --- 以下是我們為使用者註冊新增的 Serializer ---
class UserSerializerWithToken(serializers.ModelSerializer):
    # 讓 user_type 欄位可以被寫入，但不會在回傳時顯示
    user_type = serializers.CharField(write_only=True)
    # 讓 token 成為一個唯讀欄位，用來在註冊成功後回傳 token
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        # 我們需要使用者提供 username, email, password，以及我們自訂的 user_type
        fields = ['id', 'username', 'email', 'password', 'user_type', 'token']
        # 將 password 設為唯寫欄位，確保它不會被回傳
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        # 這個方法用來為新註冊的使用者產生 token
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def create(self, validated_data):
        # 這是建立新使用者的核心邏輯
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')

        # 建立 Django 內建的 User
        user = User(**validated_data)
        user.set_password(password) # 使用 set_password 來對密碼進行加密
        user.save()

        # 建立我們自訂的 Profile
        Profile.objects.create(user=user, user_type=user_type)

        return user