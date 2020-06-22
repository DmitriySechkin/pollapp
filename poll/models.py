import datetime

from django.db import models
from django.contrib.auth.models import User

from poll.utils.exceptions import *

TYPES_ANSWERS = (
    ('c', 'Choice'),
    ('t', 'Text')
)


class NewSurvey(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    @property
    def survey_questions(self):
        return self.question_set.filter(actual=True)

    def __str__(self):
        return "{}".format(self.title)


class CustomSurvey(models.Manager):

    def surveys_data(self, user):
        surveys_data = {}
        surveys_list = self.__get_user_data(user)
        unique_surveys = surveys_list.values('new_survey_id').distinct()

        for unique_result in list(unique_surveys):
            survey_id = unique_result['new_survey_id']
            survey_data = self.filter(new_survey_id=survey_id)
            title_survey = NewSurvey.objects.get(pk=survey_id)
            surveys_data[title_survey] = survey_data

        return surveys_data

    def save_answer(self, question_id, response_user, user):
        question = self.__get_question_obj(question_id)
        answer = self.__get_answer_text(question, response_user)
        self.__write_answer(question, answer, user)

    def __get_answer_text(self, question, response_user):
        if question.type_question == 'c':
            return self.__get_selected_choice(response_user, question)
        else:
            return response_user

    def __get_question_obj(self, question_id):
        try:
            return Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise NoFindQuestionByID(question_id)

    def __get_selected_choice(self, choice_answer, question):
        try:
            choice = question.choice_set.get(pk=choice_answer)
            return choice.choice_text
        except Choice.DoesNotExist:
            raise NoFindChoiceInTableById(choice_answer)

    def __write_answer(self, question, answer, user):
        try:
            survey = Survey.custom_manager.get(question=question.id, user=user)
            survey.answer = answer
            survey.pub_date = datetime.date.today()
        except Survey.DoesNotExist:
            survey = Survey(user=user,
                            question=question,
                            answer=answer,
                            new_survey_id=question.newsurvey)
        survey.save()

    def __get_user_data(self, user):
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(user=user)


class Survey(models.Model):
    new_survey_id = models.ForeignKey('NewSurvey', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    pub_date = models.DateField('date published', auto_now_add=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.TextField(max_length=400)

    custom_manager = CustomSurvey()

    class Meta:
        ordering = ['new_survey_id', 'pub_date']


class Question(models.Model):
    newsurvey = models.ForeignKey(NewSurvey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    actual = models.BooleanField()
    type_question = models.CharField(max_length=1, choices=TYPES_ANSWERS)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "{}".format(self.choice_text)
