from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Issue(models.Model):

    BUILDING_CHOICES = [
        ('SCIENCE_CENTER', 'Dorothy Westerman Herrmann Science Center'),
        ('LANDRUM', 'Landrum Academic Center'),
        ('LIBRARY', 'W. Frank Steely Library'),
        ('FINE_ARTS', 'Fine Arts Center'),
        ('BUSINESS_ACADEMIC', 'Business Academic Center'),
        ('MEP_CENTER', 'Math-Education-Psychology Center'),
        ('LUCAS_ADMIN', 'Lucas Administrative Center'),
        ('UNIVERSITY_CENTER', 'University Center and Welcome Center'),
        ('STUDENT_UNION', 'James C. and Rachel M. Votruba Student Union'),
        ('NUNN_HALL', 'Louie B. Nunn Hall'),
        ('HEALTH_INNOVATION', 'Health Innovation Center'),
        ('FOUNDERS_HALL', 'Founders Hall'),
        ('GRIFFIN_HALL', 'Griffin Hall'),
        ('REC_CENTER', 'Campus Recreation Center & Albright Health Center'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),

    ]
    CATEGORY_CHOICES = [
        ('FACILITIES', 'Facilities'),
        ('IT', 'IT/Tech'),
        ('SAFETY', 'Safety'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    report = models.ForeignKey(User, on_delete=models.CASCADE)

    building = models.CharField(max_length=100, choices=BUILDING_CHOICES)
    specific_location = models.CharField(max_length=255, blank=True, help_text="e.g., Room 201, second floor men's restroom")
    
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    photo = models.ImageField(upload_to='issue_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# Vote model
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'issue')

# model for recording issue history
class IssueHistory(models.Model):
    # Link to the issue this history log belongs to
    # related_name='history' lets us do 'issue.history.all()' later
    issue = models.ForeignKey(Issue, related_name='history', on_delete=models.CASCADE)
    
    # The user who performed the action (e.g., admin or original reporter)
    # SET_NULL means if the user is deleted, the log entry remains but this field becomes null.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # A simple description of what happened
    # e.g., "changed status from Reported to In Progress" or "created this issue"
    action_description = models.CharField(max_length=255)
    
    # The date and time this log entry was created
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This makes sure the history is always shown in the correct order (newest first)
        ordering = ['-timestamp']

    def __str__(self):
        # This is just for a nice display in the admin panel
        return f"{self.issue.title} - {self.action_description[:50]}"