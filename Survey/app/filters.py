import django_filters
from django_filters import FilterSet, Filter

from app.models import Answer, Question


class SurveyFilter(Filter):
    def filter(self, qs, value):
        if value is None:
            return qs
        questions = Question.objects.all().filter(survey=value)
        survey_query = qs.filter(question__in=questions)
        return survey_query


class AnswersFilter(FilterSet):

    survey = SurveyFilter(field_name='question')

    class Meta:
        model = Answer
        fields = ['user', 'question']
