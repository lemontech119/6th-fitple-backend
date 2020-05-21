from django.db import models
from accounts.models import User

# Create your models here.
## Tag는 나중에...
# class Tag(models.Model):
#     name = models.CharField(max_length=10, primary_key=True)
#
#     def __str__(self):
#         return self.name


class Team(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=100)
    #tags = models.ManyToManyField(Tag, related_name='teams', verbose_name='태그', blank=True)
    description = models.TextField('설명')
    status = models.CharField('상태', max_length=20)
    personnel = models.PositiveIntegerField('최대 인원')
    region = models.CharField('지역', max_length=20)
    goal = models.CharField('목표', max_length=10)
    kind = models.CharField('종류', max_length=40)
    people = models.CharField('사용고객', max_length=20)
    image = models.ImageField('이미지', upload_to="team/image/%Y/%m/%D/", default='default.jpg')
    created_at = models.DateTimeField('생성시간', auto_now_add=True)
    modified_at = models.DateTimeField('수정시간', auto_now=True)


