import pdb

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .models import Question, Survey, NewSurvey


class IndexView(LoginRequiredMixin, View):
    """ Загрузка страницы с опросами """

    def get(self, request):
        survey_list = NewSurvey.objects.all()
        template = loader.get_template('poll/index.html')

        context = {
            'survey_list': survey_list,
        }

        return HttpResponse(template.render(context, request))


def detail(request, survey_id):
    """ Загрузка страницы для прохождения опросов"""

    survey = get_object_or_404(NewSurvey, pk=survey_id, )
    if survey.survey_questions:
        return render(request, 'poll/detail.html', {'survey': survey})
    else:
        return render(request, 'poll/empty_poll.html')


def choise_save(request, question_id):
    """ Сохранение ответа"""

    question = get_object_or_404(Question, pk=question_id, )
    user = request.user
    selected_choice = question.choice_set.get(pk=request.POST['choice'])

    try:
        survey = Survey.objects.get(question=question_id)
        survey.choice = selected_choice
    except ObjectDoesNotExist:
        survey = Survey(user=user, question=question, choice=selected_choice)

    survey.save()

    return HttpResponseRedirect(
        reverse(
            'poll:detail_survey',
            args=(question.newsurvey.pk,)
        )
    )


def completed_surveys(request):
    """ Загрузка пройденных опросов """

    user = request.user

    if request.user.is_superuser:
        surveys_list = Survey.objects.all()
    else:
        surveys_list = Survey.objects.get(user=user)

    return render(
        request,
        'poll/completed_surveys.html',
        {'surveys_list': surveys_list}
    )
