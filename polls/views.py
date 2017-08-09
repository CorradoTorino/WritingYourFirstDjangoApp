from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

def get_published_questions():
    return Question.objects.filter(pub_date__lte=timezone.now())

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_last_five_published_questions(self):
        return get_published_questions().order_by('-pub_date')[:5]
    
    def get_queryset(self):
        return self.get_last_five_published_questions() 

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return get_published_questions()

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
        
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        context = {
            'question': question,
            'error_message': "You didn't select a choice"}
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

