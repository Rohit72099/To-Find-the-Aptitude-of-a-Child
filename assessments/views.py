from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Assessment, Result, Question, Response as Resp
from .serializers import AssessmentSerializer, ResultSerializer, ResponseSerializer
from users.models import ChildProfile
from django.utils import timezone


class AssessmentListView(generics.ListAPIView):
    queryset = Assessment.objects.filter(published=True)
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.AllowAny]


class AssessmentDetailView(generics.RetrieveAPIView):
    queryset = Assessment.objects.filter(published=True)
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_assessment(request, assessment_id):
    # create result for a child (child id required)
    child_id = request.data.get('child_id')
    child = get_object_or_404(ChildProfile, id=child_id)
    
    # Verify that the child belongs to the authenticated user
    from users.models import ParentProfile
    parent_profile = ParentProfile.objects.get(user=request.user)
    if child.parent != parent_profile:
        return Response({'detail': 'You do not have permission to access this child.'}, status=status.HTTP_403_FORBIDDEN)
    
    assessment = get_object_or_404(Assessment, id=assessment_id)
    result = Result.objects.create(child=child, assessment=assessment)
    return Response({'session_id': str(result.id)}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_answer(request, session_id):
    result = get_object_or_404(Result, id=session_id)
    answers = request.data.get('answers') or []
    created = []
    for item in answers:
        q_id = item.get('question')
        answer_value = item.get('answer')
        
        # Skip if question doesn't exist
        try:
            q = Question.objects.get(id=q_id)
        except Question.DoesNotExist:
            continue
            
        # Create or update response
        resp, _ = Resp.objects.get_or_create(
            result=result, 
            question=q,
            defaults={'answer': answer_value}
        )
        if not _:  # If not created (already exists), update it
            resp.answer = answer_value
            resp.save()
        
        created.append(ResponseSerializer(resp).data)
    return Response({'created': created, 'count': len(created)})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_assessment(request, session_id):
    result = get_object_or_404(Result, id=session_id)
    # naive scoring: count MCQ answers matching option marked as correct in question.options
    responses = list(result.responses.all())
    score = 0
    total = 0
    for r in responses:
        q = r.question
        total += 1
        try:
            opts = q.options or {}
            # Handle both old format (direct value) and new format (dict with 'options' and 'correct')
            if isinstance(opts, dict):
                if 'correct' in opts and 'options' in opts:
                    correct = opts.get('correct')
                else:
                    correct = opts.get('correct')
            else:
                correct = None
                
            if correct is not None and r.answer == correct:
                score += 1
                r.correct = True
            else:
                r.correct = False
            r.save()
        except Exception as e:
            print(f"Error scoring response {r.id}: {e}")
            r.correct = None
            r.save()
    raw = {'score': score, 'total': total}
    normalized = {'percent': (score / total * 100) if total else 0}
    result.raw_scores = raw
    result.normalized_scores = normalized
    result.completed_at = timezone.now()
    result.save()
    return Response(ResultSerializer(result).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_results(request, session_id):
    result = get_object_or_404(Result, id=session_id)
    return Response(ResultSerializer(result).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_results(request):
    """Get all results for the authenticated user's children"""
    from users.models import ParentProfile, ChildProfile
    
    # Get parent profile
    parent_profile, _ = ParentProfile.objects.get_or_create(user=request.user)
    
    # Get all children
    children = ChildProfile.objects.filter(parent=parent_profile)
    
    # Get all results for these children, ordered by completion date (newest first)
    results = Result.objects.filter(
        child__in=children,
        completed_at__isnull=False
    ).order_by('-completed_at').select_related('child', 'assessment')
    
    # Serialize results with additional info
    serialized_results = []
    for result in results:
        data = {
            'id': str(result.id),
            'child_id': result.child.id,
            'child_name': f"{result.child.first_name} {result.child.last_name or ''}".strip(),
            'assessment_id': result.assessment.id,
            'assessment_title': result.assessment.title,
            'started_at': result.started_at,
            'completed_at': result.completed_at,
            'raw_scores': result.raw_scores,
            'normalized_scores': result.normalized_scores,
        }
        serialized_results.append(data)
    
    return Response(serialized_results)
