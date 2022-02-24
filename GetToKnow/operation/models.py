from django.db import models

# Create your models here.
class User(models.Model):
    login_id = models.EmailField()
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = "USER"

class Question(models.Model):
    question = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "QUESTION"

class Answer(models.Model):
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "ANSWER"

class Like(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def view_count(self):
        return Like.objects.filter(answer=self).count()

    class Meta:
        db_table = "LIKE"