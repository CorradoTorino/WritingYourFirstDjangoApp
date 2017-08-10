from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question

from testUtilities import create_question
    
class QuestionModelViewTests(TestCase):
    def test_no_questions(self):
        """
        if no question are cretaed, then the message "No polls are available" is shown.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_questions(self):
        """
        if a question in the past is cretaed, then the past question is displayed.
        """
        create_question('Past Question', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question>'])
    
    def test_future_questions(self):
        """
        if a question is published in a future date, then the message "No polls are available" is shown.
        """
        create_question('Past Question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_questions(self):
        """
        if we have both a question published in the past and another published in the future,
        then we are returning only the past question.
        """
        create_question('Past Question', -30)
        create_question('Past Question', 30)
        
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question>'])

    def test_two_past_questions(self):
        """
        if we have multiple questions published in the past,
        then we are returning both of them.
        """
        create_question('Past Question 1', -30)
        create_question('Past Question 2', -15)
        
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question 2>', '<Question: Past Question 1>'])
