from rest_framework import serializers
from .models import Assessment, Section, Question, Result, Response
from users.serializers import ChildProfileSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'options', 'media_url', 'difficulty', 'time_limit', 'order')


class SectionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'order', 'questions')


class AssessmentSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ('id', 'title', 'description', 'age_min', 'age_max', 'language', 'time_limit', 'adaptive', 'published', 'version', 'sections')


class ResponseSerializer(serializers.ModelSerializer):
    question_text = serializers.SerializerMethodField()
    correct_answer_text = serializers.SerializerMethodField()
    answer_text = serializers.SerializerMethodField()

    class Meta:
        model = Response
        fields = ('id', 'result', 'question', 'question_text', 'answer', 'answer_text', 'correct', 'correct_answer_text', 'time_taken')

    def get_question_text(self, obj):
        return obj.question.text if obj.question else None

    def get_correct_answer_text(self, obj):
        if obj.question and obj.question.options:
            options_data = obj.question.options
            if isinstance(options_data, dict) and 'options' in options_data:
                correct_idx = options_data.get('correct')
                if correct_idx is not None and correct_idx < len(options_data['options']):
                    return options_data['options'][correct_idx]
        return None

    def get_answer_text(self, obj):
        if obj.question and obj.question.options:
            options_data = obj.question.options
            if isinstance(options_data, dict) and 'options' in options_data:
                if obj.answer is not None and obj.answer < len(options_data['options']):
                    return options_data['options'][obj.answer]
        return 'Unanswered'


class ResultSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Result
        fields = ('id', 'child', 'assessment', 'started_at', 'completed_at', 'raw_scores', 'normalized_scores', 'recommendations', 'responses')

