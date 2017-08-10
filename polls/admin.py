from django.contrib import admin
from .models import Choice, Question

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question',                   {'fields': ['question_text']}),
        ('DateTime Information', {'fields': ['pub_date']}),
    ]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
