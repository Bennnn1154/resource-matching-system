from django.db import models
from django.contrib.auth.models import User # 未來會用到，先 import

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