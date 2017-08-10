from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Question
   
class QuestionModeltests(TestCase):       
    def test_was_published_recently_with_future_question_return_false(self):
        """
        was_published_recently() return false when the question is pubblished in the future.
        """
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def  test_was_published_recently_with_old_question_return_false(self):
        """
        was_published_recently() return false when the question is pubblished more than one dya ago.
        """
        
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_a_question_created_in_the_last_day_return_true(self):
        """
        was_published_recently() return true when the question is pubblished in the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
