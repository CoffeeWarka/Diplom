from django.contrib import admin
from .models import Question, Answer

class AllAnswer(admin.TabularInline):
  model = Answer
  extra = 4

class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [(None, {'fields':['question_text']})]
  inlines = [AllAnswer]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)