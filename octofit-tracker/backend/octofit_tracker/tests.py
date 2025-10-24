from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Team, Activity, Workout, LeaderboardEntry

User = get_user_model()

class BasicModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user)
        self.activity = Activity.objects.create(user=self.user, team=self.team, activity_type='run', duration_minutes=10, distance_km=2.0, points=10)
        self.workout = Workout.objects.create(user=self.user, name='Morning Workout', notes='Test notes')
        self.leaderboard = LeaderboardEntry.objects.create(team=self.team, points=10)

    def test_user_created(self):
        self.assertEqual(User.objects.count(), 1)
    def test_team_created(self):
        self.assertEqual(Team.objects.count(), 1)
    def test_activity_created(self):
        self.assertEqual(Activity.objects.count(), 1)
    def test_workout_created(self):
        self.assertEqual(Workout.objects.count(), 1)
    def test_leaderboard_created(self):
        self.assertEqual(LeaderboardEntry.objects.count(), 1)
