from django.test import TestCase
from django.utils import timezone

from django.core.urlresolvers import reverse

import datetime

from .models import Question

def create_question(question_text, days):
    """
    Create a question given a question_text that is pubblished days ago.
    Days can be negative for a question pubblished in the past or positive for future question. 
    """
    time = timezone.now()+ datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionDetailViewList(TestCase):
    def test_future_question_cannot_be_shown(self):
        future_question = create_question('Future question', 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
    
class QuestionModeltests(TestCase):
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
