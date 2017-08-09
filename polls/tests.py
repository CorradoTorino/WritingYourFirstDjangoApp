from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Question

class QuestionModeltests(TestCase):
    def test_was_published_recently_with_future_question_return_false(self):
        """
        was_published_recently() return false when is the question is pubblished in the future.
        """
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
