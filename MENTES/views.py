from  django.shortcuts import render
from .models import Question , Answer, UserAnswer,Diagnose
from django.http import JsonResponse
import json
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages

def quest_and_answer(request):
    questions = Question.objects.all()
    answers = Answer.objects.values('answer_text', 'question').distinct()
    sorted_answers = sorted(answers, key=lambda x: x['answer_text'])
    print(list(sorted_answers))

    context = {
        'Question':questions,
        'Answers':sorted_answers
    }
    
    return render(request=request,template_name='questions.html',context=context)



def receive_user_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("User Answers:", data)
            diagnose = Diagnose.objects.order_by('?').first().diagnosis
            is_found = UserAnswer.objects.filter(user_answer=data).exists()
            if is_found:
                diagnose = UserAnswer.objects.get(user_answer=data).predict_diagnose
            else:
                user_answers = UserAnswer.objects.create(user=request.user, user_answer=data, predict_diagnose=diagnose)
            print(diagnose)
            
            return JsonResponse(data=diagnose, status=200, safe=False)
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format!'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=405)



# Create your views here.
def send_massage(request):
    if request.method == "POST":
        email = request.POST["email"]
        if email:
            user_answer = UserAnswer.objects.filter(user=request.user).last()
            answers = "\n".join(f"<li><strong>{a['question']}:</strong> {a['answer']}</li>" for a in user_answer.user_answer)
            diagnose = user_answer.predict_diagnose
            message = f"""
            <p><strong>Diagnosis:</strong> {diagnose}</p>
            <p><strong>Answers:</strong></p>
            <ul>{answers}</ul>
            <p><strong>Username:</strong> {request.user.username}</p>
            """
            try:
                email = EmailMultiAlternatives(
                    subject="Your Result", #!subject
                    body=message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                )
                email.attach_alternative(message, "text/html")
                email.send(fail_silently=False)
                messages.success(
                    request=request, message="Email has been sent successfully."
                )
            except Exception: # Catch the exception
                messages.error(request=request, message="Error occurred: ")
        else:
            messages.info(request=request, message="All fields are required.")
    context = {}
    return render(request, "success.html", context=context)

