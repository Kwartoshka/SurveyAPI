import json

from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import Survey, Question, Answer, TypeChoices, AnswerChoice, Choice


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

    # questions = serializers.SerializerMethodField('get_questions')
    #
    # def get_questions(self, foo):
    #     qs = Question.objects.all().filter(survey=foo.id)
    #     questions = json.loads(serialize('json', qs))
    #
    #     return questions

    class Meta:
        model = Survey
        fields = ['title', 'start_date', 'end_date', 'description',
                  # 'questions'
                  ]

    def validate(self, data):
        method = self.context["request"].method
        print(dir(self.context))
        print(self.instance)
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
    # choice_answer = ChoiceSerializer(many=True)

    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, data):
        method = self.context["request"].method

        if method in {'POST', 'PATCH', 'PUT'}:
            question_type = data['question'].type
            print(data)

            # has answer
            if 'text_answer' not in data and 'choice_answer' not in data:
                raise serializers.ValidationError('There is no answer')

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

            else:
                return data

    # def create(self, validated_data):
    #     choices = validated_data['choice_answer']
    #     instance = self.context.instance
    #     text = validated_data.get('text_answer')
    #     choice_answer = validated_data.get('text_answer')
    #     Answer.objects.create(user=validated_data['user'], question=validated_data['question'], text_answer=text,
    #                           choice_answer=choice_answer)
    #     for choice in choices:
    #         AnswerChoice.objects.create(choice_id=choice, answer_id=instance.id)
    #
    #     return instance

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        m2m_fields = []

        for attr, value in validated_data.items():

            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        for attr, value in m2m_fields:
            # if attr != 'choice_answer':

            field = getattr(instance, attr)
            field.set(value)

        #     else:
        #         answer = instance
        #         choices = Choice.objects.all().filter(answer_id=answer)
        #         relations = []
        #         new = []
        #         for choice in value:
        #             if choice not in choices:
        #                 if position[0].number != number:
        #                     updating = Position.objects.filter(product=product)
        #                     updating.update(number=number)
        #
        #                 order_sum += product.price * number
        #                 relations.append(product)
        #             else:
        #                 new_position = Position.objects.create(product=product, number=number)
        #                 new.append(new_position)
        #                 order_sum += new_position.product.price * number
        #         if relations:
        #             for position in positions:
        #
        #                 if position.product not in relations:
        #                     Position.objects.filter(id=position.id).delete()
        #         for position in new:
        #             OrderPosition.objects.create(order_id=instance.id, position_id=position.id)
        #         instance.order_sum = order_sum
        # instance.save()
        # return instance