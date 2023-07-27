from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    ADMIN = 'admin'
    MANAGER = 'manager'
    REGULAR = 'regular'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (REGULAR, 'Regular User'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=REGULAR,
    )


class Task(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-due_date",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.task.title} by {self.user.username}"


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now=True)
