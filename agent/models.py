from django.db import models
from django.utils import timezone

# Create your models here.
class Session(models.Model):
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.email

class ConversationInfo(models.Model):
    uuid = models.CharField(max_length=200)
    title = models.TextField(default="Sin titulo creado")
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='ConversationInfo')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uuid

class ConversationDetails(models.Model):
    question = models.TextField(default="")
    llm_response = models.TextField(default="")
    conversation_info_id = models.ForeignKey(ConversationInfo, on_delete=models.CASCADE, related_name='ConversationDetails')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.question

