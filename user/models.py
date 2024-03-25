from django.db import models
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, Group, Permission


class Message(models.Model):
    sender = models.CharField(max_length=50)
    message = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    isChatBox = models.BooleanField(null=False)
    document = models.ForeignKey('Document', related_name='doc', on_delete=models.CASCADE)

class Document(models.Model):
    file = models.FileField(upload_to='static/files/')
    createdDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=5)
    isActive = models.BooleanField(default=True, null=False)
    user = models.ForeignKey('CustomUser', related_name='user', on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, related_name="messages")

class Card(models.Model):
    cardNum = models.CharField(max_length=100, unique=True)
    csv = models.SmallIntegerField()
    lastDate = models.SmallIntegerField()
    activeCard = models.BooleanField(default=True)

class CustomUser(AbstractUser):
    isPremium = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True) # Hesap silme işleminde False olur ve belirli süre sonra silinir
    deleteDate = models.DateTimeField(blank=True, null=True)
    documents = models.ManyToManyField(Document, related_name="documents")
    documentCount = models.SmallIntegerField(default=0)
    card = models.ForeignKey('Card', related_name='card', on_delete=models.CASCADE, null=True, blank=True)
    
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    # user.id koymak gerek
    image = models.ImageField(upload_to = 'static/user_image', null=True, blank=True)
    
    def get_original_user_id(self):
        return self.id
    
    def delete_account(self):
        self.isActive = False
        self.deleteDate = timezone.now() + timedelta(days=30)
        self.save(update_fields=['isActive', 'deleteDate'])

    def reset_delete_date(self):
        if self.deleteDate:
            self.isActive = True
            self.deleteDate = None
            self.save(update_fields=['isActive', 'deleteDate'])

    def update_document_count(self):
        self.documentCount = self.documents.count()
        self.save(update_fields=['documentCount'])

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None

        if is_new_instance:
            self.update_document_count()  # Update document count for new instances

        super().save(*args, **kwargs)

@receiver(m2m_changed, sender=CustomUser.documents.through)
def update_document_count(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:        
        instance.update_document_count()