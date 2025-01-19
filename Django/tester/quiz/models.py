from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    question_number = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.question_text}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=50)
    right_answer = models.BooleanField(default=False)
    user_choice = models.IntegerField(default=0)

    def __str__(self):
        return f'Вариант ответа {self.question.question_text}'