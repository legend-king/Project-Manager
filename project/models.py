from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    priority = models.IntegerField(choices=[(1, "Low"), (2,"Medium"), (3, "High")])
    status = models.IntegerField(choices=[(1,"Not yet Started"), (2, "Work In Progress"),
                                           (3, "Live but modules pending"), (4, "All Modules Completed")], default=1)
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering = ('status', '-priority', '-due_date')

class ProjectModule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(choices=[(1, "Low"), (2,"Medium"), (3, "High")], default=3)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('project', 'title')
        ordering = ('completed', '-priority', '-due_date')

    def __str__(self):
        return f"{self.project} - {self.title}"
    
class ModuleTask(models.Model):
    title = models.CharField(max_length=255)
    module = models.ForeignKey(ProjectModule, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['my_order']

    def __str__(self):
        return f"{self.module} - {self.title}"
