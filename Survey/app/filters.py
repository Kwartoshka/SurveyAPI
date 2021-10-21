from django_filters import FilterSet, Filter

from .models import Answer, Question


class SurveyFilter(Filter):
    def filter(self, qs, value):
        if value == '' or value is None:
            return qs
        else:
            questions = Question.objects.all().filter(survey=value)
            survey_query = qs.filter(question__in=questions)
            return survey_query


class AnswersFilter(FilterSet):

    survey = SurveyFilter(field_name='question')

    class Meta:
        model = Answer
        fields = ['user', 'question']
