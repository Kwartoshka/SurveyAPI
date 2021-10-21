import json

from django.core.serializers import serialize
from rest_framework import serializers

from .models import Survey, Question, Answer, TypeChoices, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, data):
        method = self.context["request"].method

        if method in {'POST', 'PATCH', 'PUT'} and data['type'] not in {'TEXT', 'ONE_FIELD', 'MULTIPLE_FIELDS'}:
            raise serializers.ValidationError(f'Wrong question type')
        else:
            return data


class SurveySerializer(serializers.ModelSerializer):

    questions = serializers.SerializerMethodField('get_questions')

    def get_questions(self, foo):
        qs = Question.objects.all().filter(survey=foo.id)
        questions = json.loads(serialize('json', qs))

        return questions

    class Meta:
        model = Survey
        fields = ['id', 'title', 'start_date', 'end_date', 'description',
                  'questions'
                  ]

    def validate(self, data):
        method = self.context["request"].method
        if method == 'PATCH' and 'start_date' in data:
            if data['start_date'] != self.instance.start_date:
                raise serializers.ValidationError(f'You can not change the start_date')
            else:
                return data
        if method == 'PUT' and 'start_date' in data:
            if data['start_date'] != self.instance.start_date:
                raise serializers.ValidationError(f'You can not change the start_date')
            else:
                return data
        elif method == 'PUT' and 'start_date' not in data:
            raise serializers.ValidationError(f'Please, insert previous start_date or use "PATCH" method')
        else:
            return data


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, data):
        method = self.context["request"].method

        if method in {'POST', 'PATCH', 'PUT'}:
            question_type = data['question'].type

            # has answer
            if 'text_answer' not in data and 'choices' not in data:
                raise serializers.ValidationError('There is no answer')

            # not overanswered
            elif 'text_answer' in data and 'choices' in data:
                raise serializers.ValidationError(f'Answer must be a {question_type} only')

            # answer goes to correct field
            elif (
                    question_type == TypeChoices.TEXT
                    and 'choices' in data
                 ) or\
                    (
                        (question_type == TypeChoices.ONE or question_type == TypeChoices.MULTIPLE)
                        and 'text_answer' in data
                    ):
                raise serializers.ValidationError(f'Answer must be a {question_type}')

            # one field answer is really one:
            elif question_type == TypeChoices.ONE and len(data['choices']) > 1:
                raise serializers.ValidationError(f'It can have only one answer')

            else:
                return data


class AnswerGETSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = '__all__'
