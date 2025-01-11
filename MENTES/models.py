from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question_text  

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    user_id = models.CharField(max_length=100) 
    answer_text = models.TextField()  

    def __str__(self):
        return f"Answer to {self.question.question_text} by {self.user_id}"  

class Diagnose(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.diagnosis

class UserAnswer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user_answer = models.JSONField()
    predict_diagnose = models.CharField(max_length = 150)

    def __str__(self):
        return f"User Answer: {self.user.username}"    
