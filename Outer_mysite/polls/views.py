from multiprocessing import context
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse

from .models import Question
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
    response = "You're looking at results of question %s."
    return HttpResponse(response % question_id)

def votes(request,question_id):
    return HttpResponse("You're voting on question %s." %question_id)