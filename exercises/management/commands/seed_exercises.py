from django.core.management.base import BaseCommand
from exercises.models import Exercise


class ExerciseData:
    def __init__(self, name, description, instructions, target_muscle, equipment_required, difficulty_level, category, exercise_type, calories_burned, has_duration):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.target_muscle = target_muscle
        self.equipment_required = equipment_required
        self.difficulty_level = difficulty_level
        self.category = category
        self.exercise_type = exercise_type
        self.calories_burned = calories_burned
        self.has_duration = has_duration

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'target_muscle': self.target_muscle,
            'equipment_required': self.equipment_required,
            'difficulty_level': self.difficulty_level,
            'category': self.category,
            'exercise_type': self.exercise_type,
            'calories_burned': self.calories_burned,
            'has_duration': self.has_duration,
        }


class Command(BaseCommand):
    help = 'Seed the database with predefined exercises'

    def handle(self, *args, **kwargs):
        exercises_data = [
            ExerciseData(
                name='Push-up',
                description='A bodyweight exercise to strengthen the chest and triceps.',
                instructions='Start in a plank position, lower your chest to the ground, and push back up.',
                target_muscle='Chest',
                equipment_required='None',
                difficulty_level='Beg',
                category='Strength',
                exercise_type='ST',
                calories_burned=3,
                has_duration=False
            ),
            ExerciseData(
                name='Pull-up',
                description='An upper-body exercise targeting the back and biceps.',
                instructions='Hang from a bar with your palms facing away and pull your chin over the bar.',
                target_muscle='Back',
                equipment_required='Pull-up bar',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=5,
                has_duration=False
            ),
            ExerciseData(
                name='Squat',
                description='A lower-body exercise that targets the quadriceps, hamstrings, and glutes.',
                instructions='Stand with feet shoulder-width apart, squat down as if sitting, and return to standing.',
                target_muscle='Legs',
                equipment_required='None',
                difficulty_level='Beg',
                category='Strength',
                exercise_type='ST',
                calories_burned=2,
                has_duration=False
            ),
            ExerciseData(
                name='Running',
                description='A cardio exercise for endurance.',
                instructions='Run at a moderate pace for a set duration or distance.',
                target_muscle='Legs',
                equipment_required='None',
                difficulty_level='Int',
                category='Cardio',
                exercise_type='CA',
                calories_burned=300,
                has_duration=True
            ),
            ExerciseData(
                name='Plank',
                description='A core exercise for building abdominal and back strength.',
                instructions='Hold a plank position with your body in a straight line from head to heels.',
                target_muscle='Core',
                equipment_required='None',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=40,
                has_duration=True
            ),
            ExerciseData(
                name='Lunges',
                description='A lower-body exercise to strengthen legs and glutes.',
                instructions='Step forward with one leg, lower your hips until both knees are bent, then return to standing.',
                target_muscle='Legs',
                equipment_required='None',
                difficulty_level='Beg',
                category='Strength',
                exercise_type='ST',
                calories_burned=3,
                has_duration=False
            ),

            ExerciseData(
                name='Deadlift',
                description='A compound movement that targets the back, legs, and core.',
                instructions='Lift a barbell or dumbbells from the ground while keeping your back straight.',
                target_muscle='Back',
                equipment_required='Barbell or dumbbells',
                difficulty_level='Adv',
                category='Strength',
                exercise_type='ST',
                calories_burned=6,
                has_duration=False
            ),

            ExerciseData(
                name='Jump Rope',
                description='A cardio workout to improve endurance and coordination.',
                instructions='Swing the rope over your head and jump over it as it reaches your feet.',
                target_muscle='Full Body',
                equipment_required='Jump Rope',
                difficulty_level='Int',
                category='Cardio',
                exercise_type='CA',
                calories_burned=250,
                has_duration=True
            ),

            ExerciseData(
                name='Dips',
                description='An upper-body exercise that strengthens the triceps and chest.',
                instructions='Lower your body between parallel bars until your elbows reach 90 degrees, then push back up.',
                target_muscle='Triceps',
                equipment_required='Parallel bars',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=5,
                has_duration=False
            ),

            ExerciseData(
                name='Burpees',
                description='A full-body conditioning exercise to improve cardiovascular endurance.',
                instructions='Perform a squat, jump into a plank, do a push-up, then jump back to standing.',
                target_muscle='Full Body',
                equipment_required='None',
                difficulty_level='Adv',
                category='Cardio',
                exercise_type='CA',
                calories_burned=10,
                has_duration=False
            ),

            ExerciseData(
                name='Russian Twists',
                description='A core exercise that improves oblique strength.',
                instructions='Sit with feet lifted, twist your torso side to side while holding a weight or medicine ball.',
                target_muscle='Core',
                equipment_required='Medicine Ball (optional)',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=4,
                has_duration=False
            ),

            ExerciseData(
                name='Mountain Climbers',
                description='A high-intensity full-body exercise that increases heart rate.',
                instructions='Start in a plank position, bring knees toward your chest alternately at a fast pace.',
                target_muscle='Core',
                equipment_required='None',
                difficulty_level='Int',
                category='Cardio',
                exercise_type='CA',
                calories_burned=50,
                has_duration=True
            ),

            ExerciseData(
                name='Bench Press',
                description='A classic chest exercise that also engages triceps and shoulders.',
                instructions='Lie on a bench, lower the barbell to your chest, then push it back up.',
                target_muscle='Chest',
                equipment_required='Barbell or dumbbells',
                difficulty_level='Adv',
                category='Strength',
                exercise_type='ST',
                calories_burned=5,
                has_duration=False
            ),

            ExerciseData(
                name='Box Jumps',
                description='An explosive lower-body exercise that builds power and agility.',
                instructions='Jump onto a sturdy box or platform and land softly with bent knees.',
                target_muscle='Legs',
                equipment_required='Box',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=8,
                has_duration=False
            ),

            ExerciseData(
                name='Jump Squats',
                description='A plyometric exercise to strengthen legs and boost endurance.',
                instructions='Perform a squat and explosively jump into the air, then land back into a squat.',
                target_muscle='Legs',
                equipment_required='None',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=7,
                has_duration=False
            ),

            ExerciseData(
                name='Lat Pulldown',
                description='An upper-body strength exercise targeting the back.',
                instructions='Sit at a pulldown machine, pull the bar down to your chest, and slowly release.',
                target_muscle='Back',
                equipment_required='Pulldown machine',
                difficulty_level='Beg',
                category='Strength',
                exercise_type='ST',
                calories_burned=4,
                has_duration=False
            ),

            ExerciseData(
                name='Side Plank',
                description='A core-stabilizing exercise that strengthens obliques.',
                instructions='Lie on your side, support your body on one forearm and keep your body straight.',
                target_muscle='Core',
                equipment_required='None',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=30,
                has_duration=True
            ),

            ExerciseData(
                name='Rowing Machine',
                description='A full-body cardio exercise that mimics rowing movements.',
                instructions='Sit on the machine, pull the handle toward your chest while extending your legs.',
                target_muscle='Full Body',
                equipment_required='Rowing Machine',
                difficulty_level='Int',
                category='Cardio',
                exercise_type='CA',
                calories_burned=300,
                has_duration=True
            ),

            ExerciseData(
                name='Leg Press',
                description='A resistance exercise that targets the quadriceps, hamstrings, and glutes.',
                instructions='Sit on the machine, push the weight up with your legs, then lower it back.',
                target_muscle='Legs',
                equipment_required='Leg Press Machine',
                difficulty_level='Beg',
                category='Strength',
                exercise_type='ST',
                calories_burned=4,
                has_duration=False
            ),

            ExerciseData(
                name='Bicycle Crunches',
                description='A core exercise to strengthen the abs and obliques.',
                instructions='Lie on your back, bring opposite elbow and knee together in a cycling motion.',
                target_muscle='Core',
                equipment_required='None',
                difficulty_level='Int',
                category='Strength',
                exercise_type='ST',
                calories_burned=6,
                has_duration=False
            )

        ]

        for exercise_data in exercises_data:
            Exercise.objects.create(**exercise_data.to_dict())

        self.stdout.write(self.style.SUCCESS('Successfully seeded exercises!'))
