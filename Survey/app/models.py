from django.db import models
from datetime import date, timedelta


class TypeChoices:
    TEXT = 'TEXT'
    ONE = 'ONE_FIELD'
    MULTIPLE = 'MULTIPLE_FIELDS'


class Survey(models.Model):
    title = models.CharField(max_length=128)
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(default=date.today()+timedelta(10))
    description = models.TextField(default='')


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField(default='')
    type = models.TextField()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.TextField(default='')


class Answer(models.Model):
    # cuz surveys are anonymous we don't ask user to be authenticated, so we just ask id as number
    user = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(null=True)
    choices = models.ManyToManyField(Choice, null=True, related_name='answers')

    class Meta:
        unique_together = ('question', 'user')

