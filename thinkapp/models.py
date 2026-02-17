from django.db import models
from django.contrib.auth.models import User


class Questiondbase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class Answerdbase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Questiondbase, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to {self.question.title}"


class Commentdbase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    answer = models.ForeignKey(Answerdbase, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=200)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    

class Votingdbase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answerdbase, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField()

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.answer.id}"
    

class Profiledbase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One profile per user
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    questions = models.ManyToManyField(Questiondbase, blank=True)
    answers = models.ManyToManyField(Answerdbase, blank=True)
    about = models.TextField(blank=True)
    prof = models.CharField(max_length=50, blank=True)
    achievements = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
