from django.db import models

class Task(models.Model):
    STATUS_CHOICES = (
        ('ToDo', 'To Do'),
        ('Doing', 'Doing'),
        ('Done', 'Done'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ToDo')

    def __str__(self):
        return self.title
