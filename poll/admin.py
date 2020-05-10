from django.contrib import admin
from .models import Question, Choice, NewSurvey


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    list_display = ['votes', 'choice_text']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'actual']
    list_filter = ['newsurvey', 'actual']
    inlines = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'votes']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class NewSurveyAdmin(admin.ModelAdmin):
    list_display = ['title']
    #readonly_fields = ['user']
    inlines = [QuestionInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(NewSurvey, NewSurveyAdmin)
