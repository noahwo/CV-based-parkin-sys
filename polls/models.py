from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now() 
        
        # Judge if the pub_date is with in one day
        return now >= self.pub_date >= now - datetime.timedelta(days=1)
        
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    """
    __str__() is important for models, it
        1) Bring conviniencf in  shell 
        2) Used also in admin for representing object
    """
    
    def __str__(self):
        return self.choice_text