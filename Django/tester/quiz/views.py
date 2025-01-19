from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from django.db.models import F
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm
from django.core.paginator import Paginator

@login_required
def home(request):
    all_questions = Question.objects.all()
    paginator = Paginator(all_questions, 6)
    page_number = request.GET.get('page')
    page_quest = paginator.get_page(page_number)
    return render(request, "quiz/home.html", {'all_questions': all_questions, 'page_quest': page_quest})


@login_required
def choose_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "quiz/quest.html", {"question": question})

@login_required
def question_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "quiz/answer.html", {"question": question})

@login_required
def user_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        return render(request, 'quiz/quest.html', {'question': question, 'error_message': 'Выбери один!'})
    else:
        selected_answer.user_choice = F('user_choice') + 1
        selected_answer.save()
        return HttpResponseRedirect(reverse('answer', args=(question.id,)))

def user_login(request):
    return render(request, 'quiz/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'quiz/register.html', {'form': form})