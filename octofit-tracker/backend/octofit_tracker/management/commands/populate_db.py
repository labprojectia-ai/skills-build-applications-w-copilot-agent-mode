from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from octofit_tracker.models import Team, Activity, Workout, LeaderboardEntry
from django.db import transaction
import pymongo

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data (superheroes, teams Marvel and DC)'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')

        with transaction.atomic():
            # Remove existing demo data (teams, activities, workouts, leaderboard entries)
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            LeaderboardEntry.objects.all().delete()
            Team.objects.all().delete()

            # Optionally remove demo users we create (non-superuser and emails matching our demo domain)
            # Use email__contains to avoid database operators unsupported by djongo
            try:
                demo_users = User.objects.filter(is_superuser=False, email__contains='@example')
                if demo_users.exists():
                    demo_users.delete()
            except Exception:
                # If filtering fails for any reason, continue without deletion
                pass

            # Create teams
            marvel = Team.objects.create(name='Marvel')
            dc = Team.objects.create(name='DC')

            # Create demo users (superheroes)
            users_data = [
                ('tony@marvel.example', 'IronMan', marvel),
                ('thor@marvel.example', 'Thor', marvel),
                ('steve@marvel.example', 'CaptainAmerica', marvel),
                ('bruce@dc.example', 'Batman', dc),
                ('clark@dc.example', 'Superman', dc),
                ('diana@dc.example', 'WonderWoman', dc),
            ]

            created_users = []
            for email, username, team in users_data:
                user = User.objects.create_user(username=username, email=email, password='password123')
                team.members.add(user)
                created_users.append((user, team))

            # Create activities for each user
            for user, team in created_users:
                # simple sample activities
                Activity.objects.create(user=user, team=team, activity_type='run', duration_minutes=30, distance_km=5.0, points=50)
                Activity.objects.create(user=user, team=team, activity_type='strength', duration_minutes=45, points=40)

            # Compute leaderboard points per team
            for team in [marvel, dc]:
                total = 0
                for a in team.activities.all():
                    total += a.points
                LeaderboardEntry.objects.create(team=team, points=total)

        # Create unique index on user email using pymongo (best-effort)
        try:
            client = pymongo.MongoClient('mongodb://localhost:27017')
            db = client['octofit_db']
            # Djongo often stores users in auth_user collection
            if 'auth_user' in db.list_collection_names():
                db.auth_user.create_index([('email', pymongo.ASCENDING)], unique=True, name='unique_email')
            # Also try common users collection name
            if 'users' in db.list_collection_names():
                db.users.create_index([('email', pymongo.ASCENDING)], unique=True, name='unique_email_users')
            client.close()
            self.stdout.write(self.style.SUCCESS('Created unique index on user email (if collection existed)'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create index via pymongo: {e}'))

        self.stdout.write(self.style.SUCCESS('Database population complete.'))
