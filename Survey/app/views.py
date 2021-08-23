from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .filters import AnswersFilter
from .models import Survey, Question, Answer, Choice
from .serializers import SurveySerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer, AnswerGETSerializer


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAdminUser()]
        return []


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsAdminUser()]
        return []


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnswersFilter

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsAdminUser()]
        return []

    def get_serializer_class(self):
        print(self.action)
        if self.action in {"list", 'retrieve'}:
            return AnswerGETSerializer
        else:
            return AnswerSerializer


class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
