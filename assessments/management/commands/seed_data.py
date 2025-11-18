from django.core.management.base import BaseCommand
from assessments.models import Assessment, Section, Question
from users.models import ParentProfile, ChildProfile
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed sample assessment and user data'

    def handle(self, *args, **options):
        # Create sample parent and child
        user, _ = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'Parent'
            }
        )
        user.set_password('demo123')
        user.save()
        
        parent_profile, _ = ParentProfile.objects.get_or_create(user=user)
        
        child, _ = ChildProfile.objects.get_or_create(
            parent=parent_profile,
            first_name='Sarah',
            defaults={
                'last_name': 'Smith',
                'dob': datetime.now().date() - timedelta(days=365*10),
                'gender': 'female',
                'grade': '5'
            }
        )

        # Create sample assessments
        assessment1, _ = Assessment.objects.get_or_create(
            title='Numerical Aptitude Test',
            defaults={
                'description': 'Test your mathematical and numerical reasoning abilities',
                'age_min': 8,
                'age_max': 16,
                'language': 'en',
                'time_limit': 20,
                'adaptive': False,
                'published': True,
                'version': '1.0'
            }
        )

        assessment2, _ = Assessment.objects.get_or_create(
            title='Verbal Reasoning Test',
            defaults={
                'description': 'Assess your language and comprehension skills',
                'age_min': 8,
                'age_max': 18,
                'language': 'en',
                'time_limit': 25,
                'adaptive': False,
                'published': True,
                'version': '1.0'
            }
        )

        # Add sections and questions to first assessment
        section1, _ = Section.objects.get_or_create(
            assessment=assessment1,
            order=1,
            defaults={'title': 'Basic Arithmetic'}
        )

        questions = [
            {
                'text': 'What is 15 + 27?',
                'options': ['32', '42', '52', '62'],
                'correct': 1
            },
            {
                'text': 'What is 45 - 18?',
                'options': ['17', '27', '37', '47'],
                'correct': 1
            },
            {
                'text': 'What is 12 × 5?',
                'options': ['50', '55', '60', '65'],
                'correct': 2
            },
            {
                'text': 'What is 100 ÷ 4?',
                'options': ['20', '25', '30', '35'],
                'correct': 1
            },
            {
                'text': 'What is 20% of 150?',
                'options': ['20', '25', '30', '35'],
                'correct': 2
            },
        ]

        for idx, q_data in enumerate(questions, 1):
            Question.objects.get_or_create(
                section=section1,
                text=q_data['text'],
                order=idx,
                defaults={
                    'type': 'mcq',
                    'options': {'options': q_data['options'], 'correct': q_data['correct']},
                    'difficulty': 0.5,
                    'time_limit': 2
                }
            )

        # Add sections and questions to second assessment
        section2, _ = Section.objects.get_or_create(
            assessment=assessment2,
            order=1,
            defaults={'title': 'Reading Comprehension'}
        )

        verbal_questions = [
            {
                'text': 'Choose the word that means the opposite of "bright":',
                'options': ['Dark', 'Light', 'Shiny', 'Clear'],
                'correct': 0
            },
            {
                'text': 'Which sentence is grammatically correct?',
                'options': [
                    'She go to school every day',
                    'She goes to school every day',
                    'She going to school every day',
                    'She gone to school every day'
                ],
                'correct': 1
            },
            {
                'text': 'What does the phrase "piece of cake" mean?',
                'options': [
                    'A slice of dessert',
                    'Something very difficult',
                    'Something very easy',
                    'A baking ingredient'
                ],
                'correct': 2
            },
        ]

        for idx, q_data in enumerate(verbal_questions, 1):
            Question.objects.get_or_create(
                section=section2,
                text=q_data['text'],
                order=idx,
                defaults={
                    'type': 'mcq',
                    'options': {'options': q_data['options'], 'correct': q_data['correct']},
                    'difficulty': 0.6,
                    'time_limit': 2
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully seeded data!\n'
                'Demo account:\n'
                '  Username: demo\n'
                '  Password: demo123\n'
                '  Email: demo@example.com\n'
                f'Child: {child.first_name} {child.last_name}\n'
                f'Assessments: {assessment1.title}, {assessment2.title}'
            )
        )
