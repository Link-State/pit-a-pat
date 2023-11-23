from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.

# 롤링페이퍼 테이블
class Rolling_paper(models.Model) :
    paper_number = models.AutoField(primary_key=True)
    nickname = models.ForeignKey(User, on_delete=models.CASCADE, to_field="nickname", db_column="nickname")
    subject = models.CharField(max_length=50)
    users = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(null=True)

    class Meta :
        db_table = "Paper"
