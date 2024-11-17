from django.db import models
from accounts.models import User,Profile
# Create your models here.

# Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the quiz.")
    description = models.TextField(blank=True, null=True, help_text="Description of the quiz.")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    start_time = models.DateTimeField(help_text="Start time of the quiz.")
    end_time = models.DateTimeField(help_text="End time of the quiz.")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_active(self):
        """Checks if the quiz is currently active based on start and end time."""
        current_time = now()
        return self.start_time <= current_time <= self.end_time

    def has_ended(self):
        """Checks if the quiz has ended."""
        return now() > self.end_time

    def has_started(self):
        """Checks if the quiz has started."""
        return now() >= self.start_time


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(help_text="Text of the question.")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]


# Choice Model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255, help_text="Choice text.")
    is_correct = models.BooleanField(default=False, help_text="Is this choice the correct answer?")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


# Submission Model
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="submissions")
    start_time = models.DateTimeField(auto_now_add=True, help_text="Start time of the user's submission.")
    duration = models.DurationField(default=timedelta(minutes=30), help_text="Allowed time duration for the submission.")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.quiz.title}"

    def is_within_time_limit(self):
        """Checks if the submission is within the allowed time duration."""
        end_time = self.start_time + self.duration
        return now() <= end_time


# Answer Model
class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answers")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.submission.user.phone_number} - {self.question.text[:50]}"