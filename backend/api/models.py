from django.db import models
from django.contrib.auth.models import User # 未來會用到，先 import

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('university', '大學端'),
        ('school', '國高中小端'),
    )
    # 與 User 模型建立一對一的關聯，代表每個 User 都會有一個 Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name="使用者類別")

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"


class Project(models.Model):
    # 我們先用比較簡單的欄位，之後可以再擴充
    title = models.CharField(max_length=200, verbose_name="計畫標題")
    description = models.TextField(verbose_name="計畫簡介")
    subject = models.CharField(max_length=50, verbose_name="主題類別", help_text="例如：科學、藝術、語文")
    participant_limit = models.PositiveIntegerField(default=30, verbose_name="人數限制")
    restrictions = models.TextField(blank=True, verbose_name="其他限制", help_text="例如：限國中生、需自備筆電")
    
    # 未來可以加上 owner = models.ForeignKey(User, on_delete=models.CASCADE) 來記錄是誰上傳的
    status = models.CharField(
        max_length=20,
        choices=[('pending', '審核中'), ('approved', '已上架'), ('closed', '已結束')],
        default='pending',
        verbose_name="狀態"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return self.title

class Application(models.Model):
    # 關聯到申請的計畫，如果計畫被刪除，相關的申請也會一併刪除
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications', verbose_name="申請計畫")
    # 關聯到申請者(User)，如果使用者被刪除，申請也會一併刪除
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name="申請人")
    
    # 申請表單的欄位
    contact_person = models.CharField(max_length=100, verbose_name="學校聯絡人")
    contact_email = models.EmailField(verbose_name="聯絡 Email")
    contact_phone = models.CharField(max_length=20, verbose_name="聯絡電話")
    notes = models.TextField(blank=True, verbose_name="備註事項")
    
    # 申請狀態
    STATUS_CHOICES = (
        ('pending', '待審核'),
        ('approved', '已核准'),
        ('rejected', '已拒絕'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="申請狀態")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="申請時間")

    def __str__(self):
        return f"{self.applicant.username} 申請 {self.project.title}"