from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question',                   {'fields': ['question_text']}),
        ('DateTime Information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    
    list_display = ('question_text', 'pub_date', 'was_published_recently')

admin.site.register(Question, QuestionAdmin)

