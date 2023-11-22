from django.db import models
from users.models import User

# Create your models here.

# 메세지 테이블
class Message(models.Model) :
    message_number = models.AutoField(primary_key=True)
    paper_number = models.IntegerField()
    nickname = models.ForeignKey(User, on_delete=models.CASCADE, to_field="nickname", db_column="nickname")
    content = models.CharField(max_length=500, blank=True)
    wrote = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta :
        db_table = "Message"
        constraints = []
