# tracker/admin.py
from django.contrib import admin
from .models import Issue, Vote, IssueHistory  

admin.site.register(Issue)
admin.site.register(Vote)
admin.site.register(IssueHistory)