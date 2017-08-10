from django.utils import timezone

import datetime

from .models import Question

def create_question(question_text, days):
    """
    Create a question given a question_text that is pubblished days ago.
    Days can be negative for a question pubblished in the past or positive for future question. 
    """
    time = timezone.now()+ datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)