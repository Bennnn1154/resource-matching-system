from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Project, Application
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ProjectSerializer(serializers.ModelSerializer):
    # --- 欄位定義維持不變 ---
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    application_count = serializers.SerializerMethodField(read_only=True)
    applicants = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'subject', 'participant_limit', 
                  'restrictions', 'status', 'created_at', 'owner', 'owner_username', 
                  'application_count', 'applicants']
        read_only_fields = ['owner']
    
    def get_application_count(self, obj):
        return obj.applications.count()

    # --- 👇👇👇 關鍵修改點在這裡 👇👇👇 ---
    def get_applicants(self, obj):
        # 取得所有關聯的 Application 物件
        applications = obj.applications.all()
        # 使用 ApplicationSerializer 來序列化這些物件
        # many=True 表示我們正在序列化一個物件列表
        return ApplicationSerializer(applications, many=True).data

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
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 繼承父類別的 get_token 方法，拿到原始的 token
        token = super().get_token(user)

        # 在 token 的 payload 中，加入我們想要的自訂欄位
        token['username'] = user.username
        # 透過 user.profile 來反向查詢到關聯的 Profile 模型，並取得 user_type
        try:
            token['user_type'] = user.profile.user_type
        except user.profile.RelatedObjectDoesNotExist:
            # 處理例外情況，例如 admin 使用者可能沒有 profile
            token['user_type'] = None 

        return token

class ApplicationSerializer(serializers.ModelSerializer):
    # 讓 applicant 欄位在回傳時，顯示使用者名稱，而不是 ID
    applicant_username = serializers.CharField(source='applicant.username', read_only=True)

    class Meta:
        model = Application
        # applicant 欄位會由後端自動填入，不需要前端提供
        fields = ['id', 'project', 'applicant', 'applicant_username', 'contact_person', 'contact_email', 'contact_phone', 'notes', 'status', 'applied_at']
        read_only_fields = ['applicant', 'status', 'applied_at']