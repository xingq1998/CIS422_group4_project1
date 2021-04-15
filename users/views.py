from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template('users/index.html')
    context = {
        'latest_question_list': [{"id": 1, "question_text": "text"}, {"id": 2, "question_text": "text2"}],
    }
    return HttpResponse(template.render(context, request))


#    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    return render(request, 'users/detail.html', {'question': question_id})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
