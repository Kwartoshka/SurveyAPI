from django.db import models


class TypeChoices(models.TextChoices):

    TEXT = 'TEXT', 'Text answer'
    ONE = 'ONE_FIELD', 'One field answer'
    MULTIPLE = 'MULT_Field', 'Multiple fields answer'


class Survey(models.Model):
    title = models.CharField(max_length=128)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=start_date)
    description = models.TextField(default='')


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField(default='')
    type = models.TextField(choices=TypeChoices.choices)


class Answer(models.Model):
    user = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(null=True)
    choice_answer = models.TextField(null=True)

    class Meta:
        unique_together = ('question', 'user')
