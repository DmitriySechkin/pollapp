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


class Detail(LoginRequiredMixin, View):
    def get(self, request, survey_id):
        survey = get_object_or_404(NewSurvey, pk=survey_id, )

        if survey.survey_questions:
            return render(request, 'poll/detail_test.html', {'survey': survey})
        else:
            return render(request, 'poll/empty_poll.html')

    def post(self, request, survey_id):
        user = request.user
        survey = get_object_or_404(NewSurvey, pk=survey_id, )
        for question_id, response_user in iter(request.POST.items()):
            if question_id == 'csrfmiddlewaretoken':
                continue
            Survey.custom_manager.save_answer(question_id, response_user, user)

        return render(request, 'poll/detail_test.html', {'survey': survey})


def completed_surveys(request):
    """ Загрузка пройденных опросов """

    user = request.user
    surveys_list = Survey.custom_manager.surveys_data(user)
    for survey, data_survey in iter(surveys_list.items()):
        for answer in data_survey:
            print(answer.user)

    return render(
        request,
        'poll/completed_surveys.html',
        {'surveys_list': surveys_list}
    )
