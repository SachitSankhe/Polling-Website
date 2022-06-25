from django.urls import reverse
from multiprocessing import context
from random import choices
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect

from .models import Question, Choices
# Create your views here.


def index(request):
    latest_questions_list = Question.objects.order_by('pub_date')[:5]
    #To use inbuilt template
    # output = ", ".join([q.question_text for q in latest_questions_list])
    # return HttpResponse(output)
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_questions_list,
    }
    return HttpResponse(template.render(context, request))
    #Shortcut
    # context = {
    #     'latest_question_list': latest_questions_list,
    # }
    # return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except:
    #     raise Http404("Question does not exist")
    # return render(request,"polls/details.html",{'question':question})
    #Shortcut
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/details.html", {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def votes(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices_set.get(pk=request.POST['choice'])
    except(KeyError, Choices.DoesNotExist):
        #Redisplaying the quesion voting form
        return render(request, 'polls/details.html', {'question': question, 'error_message': "You didnt select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
