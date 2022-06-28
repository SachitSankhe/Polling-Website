from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Question, Choices
# Create your views here.


class IndexView(generic.ListView):
    # latest_questions_list = Question.objects.order_by('pub_date')[:5]
    #To use inbuilt template
    # output = ", ".join([q.question_text for q in latest_questions_list])
    # return HttpResponse(output)

    # To use custom template
    # template = loader.get_template('polls/index.html')
    # context = {
    # 'latest_question_list': latest_questions_list,
    # }
    # return HttpResponse(template.render(context, request))

    #Shortcut
    # context = {
    #     'latest_question_list': latest_questions_list,
    # }
    # return render(request, 'polls/index.html', context)

    # Using generic views
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five questions
        return Question.objects.order_by('pub_date')[:5]


class DetailView(generic.DetailView):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except:
    #     raise Http404("Question does not exist")
    # return render(request,"polls/details.html",{'question':question})
    #Shortcut
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, "polls/details.html", {'question': question})

    #Using Generic View
    model = Question
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question': question})

    #USe generic views
    model = Question
    template_name = 'polls/results.html'

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
    return HttpResponseRedirect(reverse('results', args=(question_id,)))
