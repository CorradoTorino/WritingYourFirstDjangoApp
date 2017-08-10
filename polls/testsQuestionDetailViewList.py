from django.test import TestCase
from django.core.urlresolvers import reverse

from testUtilities import create_question

class QuestionDetailViewList(TestCase):
    def test_future_question_cannot_be_shown(self):
        future_question = create_question('Future question', 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
    