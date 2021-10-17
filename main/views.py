import django.contrib.auth as auth
from django.shortcuts import render, redirect


from main import forms, models, utils


def index(request):
    questions_list = models.Question.objects.new()
    page = request.GET.get('page')

    return render(request, 'index.html', {
        'questions': utils.paginate(questions_list, page, 4), 'popular_tags': models.Tag.objects.popular()[:3],
        'top_users': models.User.objects.top()[:3],
    })


def hot(request):
    questions_list = models.Question.objects.hot()
    page = request.GET.get('page')

    return render(request, 'hot.html', {
        'questions': utils.paginate(questions_list, page, 4), 'popular_tags': models.Tag.objects.popular()[:3],
        'top_users': models.User.objects.top()[:3],
    })


def ask(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method != 'POST':
        return render(request, 'questions/ask.html')

    title = request.POST.get('title', '')
    text = request.POST.get('text', '')
    tags_titles = request.POST.get('tags', '').split(', ')

    question = models.Question(author=request.user, title=title, text=text)
    question.save()

    question.create_tags(tags_titles)

    return redirect('/question/' + str(question.id))


def question(request, id):
    question = models.Question.objects.get(pk=id)
    answers_list = models.Answer.objects.filter(question_id=id)
    page = request.GET.get('page')

    return render(request, 'questions/question.html', {
        'question': question,
        'answers': utils.paginate(answers_list, page, 3),
    })


def answer(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method != 'POST':
        return redirect('/question/' + str(id))

    text = request.POST.get('text', '')

    question = models.Question.objects.get(pk=id)
    answer = models.Answer(author=request.user, quest=question, text=text)
    answer.save()

    max_page = utils.get_paginated_max_pax(models.Answer.objects.filter(quest=id), 3)

    return redirect('/question/{}/?page={}'.format(id, max_page))


def tag(request, id):
    current_tag = models.Tag.objects.get(pk=id)
    questions_list = current_tag.get_questions()
    page = request.GET.get('page')

    return render(request, 'questions/tag.html', {
        'current_tag': current_tag, 'questions': utils.paginate(questions_list, page, 4),
        'popular_tags': models.Tag.objects.popular()[:3], 'top_users': models.User.objects.top()[:3],
    })


def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect('/')

    args = {}

    user = request.user
    args['form'] = forms.ProfileEditForm(initial={
        'username': user.username, 'email': user.email,
        'nickname': user.nickname, 'avatar': user.avatar,
    })

    if request.method != 'POST':
        return render(request, 'profile/edit.html', args)

    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    nickname = request.POST.get('nickname', '')
    avatar = utils.save_file(request.FILES.get('avatar'))

    if len(models.User.objects.filter(username=username)) != 0:
        args['error'] = 'User with the same username already exists'
        return render(request, 'profile/edit.html', args)

    if len(models.User.objects.filter(email=email)) != 0:
        args['error'] = 'User with the same email already exists'
        return render(request, 'profile/edit.html', args)

    user.username = username
    user.email = email
    user.nickname = nickname
    user.avatar = utils.save_file(avatar)

    user.save

    return render(request, 'profile/edit.html', args)


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    args = {}
    args['form'] = forms.LoginForm()

    if request.method != 'POST':
        return render(request, 'profile/login.html', args)

    user = auth.authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))

    if user is None:
        args['error'] = 'Username or password is invalid'
        return render(request, 'profile/login.html', args)

    auth.login(request, user)

    return redirect('/')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    args = {}
    args['form'] = forms.SignupForm()

    if request.method != 'POST':
        return render(request, 'profile/login.html', args)

    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    nickname = request.POST.get('nickname', '')
    password = request.POST.get('password', '')
    reapeat = request.POST.get('reapeat', '')
    avatar_file = request.FILES.get('avatar')

    if len(models.User.objects.filter(username=username)) != 0:
        args['error'] = 'User with the same username already exists'
        return render(request, 'profile/signup.html', args)

    if len(models.User.objects.filter(email=email)) != 0:
        args['error'] = 'User with the same email already exists'
        return render(request, 'profile/signup.html', args)

    if password != reapeat:
        args['error'] = 'Passwords mismatch'
        return render(request, 'profile/signup.html', args)

    user = models.User.objects.create_user(
        username=username, email=email, nickname=nickname,
        password=password, avatar=utils.save_file(avatar_file)
    )

    auth.login(request, user)

    return redirect('/')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('/')
