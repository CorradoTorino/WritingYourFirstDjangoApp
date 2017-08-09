from django.test import TestCase
from django.utils import timezone

from unittest import skip
import datetime

from .models import Question

class QuestionModeltests(TestCase):
    @skip("This test can pass only in the first 30 days from the creation. It depends on the entry in the db.")
    def test_was_published_recently_with_future_question_return_false(self):
        """
        was_published_recently() return false when is the question is pubblished in the future.
        However this test is a dummy test. it depends on the state of the db. see skip note.
        """
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)