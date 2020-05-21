from django.db import models
from django.contrib.auth.models import User

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
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)

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
