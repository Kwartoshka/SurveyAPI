import json

from django.core.serializers import serialize
from rest_framework import serializers

from .models import Survey, Question, Answer, TypeChoices


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('get_questions')

    def get_questions(self, foo):
        qs = Question.objects.all().filter(survey=foo.id)
        questions = json.loads(serialize('json', qs))

        return questions

    class Meta:
        model = Survey
        fields = ['title', 'start_date', 'end_date', 'description', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, data):
        method = self.context["request"].method

        if method in {'POST', 'PATCH', 'PUT'}:
            question_type = data['question'].type

            # has answer
            if 'text_answer' not in data and 'choice_answer' not in data:
                raise serializers.ValidationError(f'There is no answer')

            # not overanswered
            elif 'text_answer' in data and 'choice_answer' in data:
                raise serializers.ValidationError(f'Answer must be a {question_type} only')

            # answer goes to correct field
            elif (
                    question_type == TypeChoices.TEXT
                    and 'choice_answer' in data
                 ) or\
                    (
                        (question_type == TypeChoices.ONE or question_type == TypeChoices.MULTIPLE)
                        and 'text_answer' in data
                    ):
                raise serializers.ValidationError(f'Answer must be a {question_type}')

            # one field answer is really one:
            elif question_type == TypeChoices.ONE and len(data['choice_answer']) > 1:
                raise serializers.ValidationError(f'It can have only one answer')

            elif question_type == TypeChoices.ONE and len(data['choice_answer']) > 1:
                raise serializers.ValidationError(f'It can have only one answer')
            else:
                return data
