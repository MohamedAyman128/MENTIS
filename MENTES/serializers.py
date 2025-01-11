from rest_framework import serializers
from .models import Questions
from .models import Answers  # استيراد النموذج المرتبط

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'  # أو حدد الحقول بشكل مباشر إذا كنت تريد تخصيصها
