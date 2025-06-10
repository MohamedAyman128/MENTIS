from  django.shortcuts import render
from .models import Question , Answer, UserAnswer,Diagnose
from django.http import JsonResponse
import json
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
import joblib
import numpy as np
import os

def quest_and_answer(request):
    questions = Question.objects.order_by('id')
    # جلب كل الأسئلة حتى لو لم يكن لها إجابات
    answers = Answer.objects.order_by('question', 'answer_text')
    unique_answers = []
    seen = set()
    for ans in answers:
        key = (ans.question_id, ans.answer_text.strip())
        if key not in seen:
            unique_answers.append(ans)
            seen.add(key)
    # طباعة الأسئلة التي ليس لها أي إجابة
    questions_with_answers = set(a.question_id for a in unique_answers)
    questions_without_answers = [q for q in questions if q.id not in questions_with_answers]
    print('Questions WITHOUT answers:', questions_without_answers)
    context = {
        'Question': questions,
        'Answers': unique_answers
    }
    return render(request=request, template_name='questions.html', context=context)



def receive_user_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("User Answers:", data)

            # تجهيز البيانات بنفس ترتيب الأعمدة المستخدمة في التدريب
            # يفترض أن data عبارة عن قائمة من dicts: [{question: ..., answer: ...}, ...]
            # أو dict: {feature: value, ...}
            if isinstance(data, dict):
                features = [data.get(f, 0) for f in MODEL_FEATURES]
            elif isinstance(data, list):
                # إذا كانت قائمة أسئلة/إجابات
                answer_map = {item['question']: item['answer'] for item in data if 'question' in item and 'answer' in item}
                features = [answer_map.get(f, 0) for f in MODEL_FEATURES]
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format!'}, status=400)

            # تحويل القيم الرقمية إذا لزم الأمر
            features = [int(x) if str(x).isdigit() else 0 for x in features]
            X = np.array(features).reshape(1, -1)
            prediction = model.predict(X)[0]

            # حفظ النتيجة
            is_found = UserAnswer.objects.filter(user_answer=data).exists()
            if is_found:
                diagnose = UserAnswer.objects.get(user_answer=data).predict_diagnose
            else:
                diagnose = prediction
                UserAnswer.objects.create(user=request.user, user_answer=data, predict_diagnose=str(diagnose))
            # تحويل أي قيمة رقمية إلى اسم التشخيص حسب طلب المستخدم
            diagnosis_map = {
                0: "Normal",
                1: "Depression",
                2: "Bipolar Type-1",
                3: "Bipolar Type-2"
            }
            try:
                diagnosis_index = int(diagnose)
                diagnosis_label = diagnosis_map.get(diagnosis_index, str(diagnose))
            except Exception:
                diagnosis_label = str(diagnose)
            print('Diagnosis label:', diagnosis_label)
            return JsonResponse(diagnosis_label, safe=False, status=200)
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
            # تحويل رقم التشخيص إلى اسم المرض
            diagnosis_map = {
                "0": "Normal",
                "1": "Depression",
                "2": "Bipolar Type-1",
                "3": "Bipolar Type-2"
            }
            diagnosis_label = diagnosis_map.get(str(diagnose), str(diagnose))
            message = f"""
            <p><strong>Diagnosis:</strong> {diagnosis_label}</p>
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

# تحميل النموذج مرة واحدة عند بدء التشغيل
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'random_forest_model_96.pkl')
model = joblib.load(MODEL_PATH)

# قائمة الخصائص المطلوبة بنفس ترتيب التدريب
MODEL_FEATURES = [
    'Age',
    'Gender',
    'Sleep Disorder',
    'Mood Disorder',
    'Anxiety Disorder',
    'Schizophrenia',
    'Eating Disorder',
    'ADHD',
    'PTSD',
    'OCD',
    'Autism',
    'Bipolar Disorder',
    'Substance Abuse',
    'Personality Disorder',
    'Dementia',
    'Suicidal thoughts',
    'Family History'
]

