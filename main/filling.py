import os
import random
import django

from django.contrib.auth import get_user_model
from faker import Faker

from main import models


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forum.settings")
django.setup()
User = get_user_model()
fake = Faker()


def create_users(n):
    for _ in range(n):
        u = User.objects.create_user(username=fake.user_name(), email=fake.email(), password="secret_password")
        u.save()


def create_tags(n):
    for _ in range(n):
        t = models.Tag(title=fake.word())
        t.save()


def create_questions(n):
    users_id_list = [user.pk for user in User.objects.all()]
    tags_id_list = [tag.pk for tag in models.Tag.objects.all()]

    for _ in range(n):
        user_id = random.choice(users_id_list)

        q = models.Question(author_id=user_id, title=fake.sentence(), text=fake.text())
        q.save()

        for _ in range(random.randint(1, 3)):
            t_id = random.choice(tags_id_list)
            q.tags.add(t_id)

        create_answers(random.randint(1, 10), q, users_id_list)
        create_likes(random.randint(1, 20), q, users_id_list, 'QuestionLike')


def create_answers(n, question, users_id_list):
    for _ in range(n):
        user_id = random.choice(users_id_list)
        a = models.Answer(author_id=user_id, question=question, text=fake.text())
        a.save()

        create_likes(random.randint(1, 10), a, users_id_list, 'AnswerLike')


def create_likes(n, resource, users_id_list, likes_type):
    for _ in range(n):
        user_id = random.choice(users_id_list)

        if likes_type == 'QuestionLike':
            l = models.QuestionLike(author_id=user_id, question=resource, liked=True)
        elif likes_type == 'AnswerLike':
            l = models.AnswerLike(author_id=user_id, answer=resource, liked=True)

        l.save()


create_users(10000)
create_tags(10000)
create_questions(100000)
