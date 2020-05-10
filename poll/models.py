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


class Survey(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    pub_date = models.DateField('date published', auto_now_add=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)


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
