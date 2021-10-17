from django.db import models
from django.db.models import Count
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.models import ContentType


class UserManager(UserManager):
    def top(self):
        top_user_ids = Answer.objects.get_user_ids()
        return list(map(lambda top_user_id: self.get(pk=top_user_id['author']), top_user_ids))


class TagManager(models.Manager):
    def _with_questions(self):
        return self.all().annotate(cnt=Count('question'))

    def popular(self):
        return self._with_questions().order_by('-cnt')


class QuestionManager(models.Manager):
    def _with_likes(self):
        return self.all().annotate(cnt=Count('questionlike'))

    def new(self):
        return self.all().order_by('date')

    def hot(self):
        return self._with_likes().order_by('-cnt')


class AnswerManager(models.Manager):
    def _with_author(self):
        return self.all().annotate(cnt=Count('author'))

    def get_user_ids(self):
        return self._with_author().order_by('-cnt').values('author').distinct()


class User(AbstractUser):
    avatar = models.ImageField(null=False, default='/static/users_avatar/default.png')
    nickname = models.CharField(max_length=20, null=False, default='name')

    objects = UserManager()


class Tag(models.Model):
    title = models.CharField(max_length=32, null=False)

    objects = TagManager()

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all()


class Question(models.Model):
    title = models.CharField(max_length=96, null=False)
    text = models.TextField(max_length=960, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    date = models.DateField(auto_now=True)

    objects = QuestionManager()

    def get_likes_count(self):
        return self.questionlike_set.all().count()

    def get_answers_count(self):
        return self.answer_set.all().count()

    def create_tags(self, tags_titles):
        tags = []
        for tag_title in tags_titles:
            tags_array = Tag.objects.filter(title=tag_title)
            if len(tags_array) == 0:
                tag = Tag(title=tag_title)
                tag.save()
            else:
                tag = tags_array[0]

            tags.append(tag)

        for tag in tags:
            self.tags.add(tag)


class Answer(models.Model):
    text = models.TextField(max_length=960)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = AnswerManager()

    def get_likes_count(self):
        return self.answerlike_set.all().count()


class QuestionLike(models.Model):
    liked = models.BooleanField(null=False, default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    liked = models.BooleanField(null=False, default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
