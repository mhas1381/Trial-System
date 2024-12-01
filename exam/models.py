from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import pandas as pd
import random
from accounts.models import User


class TabChange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tab_changes = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def add_tab_change(self, action, user_agent, ip_address):
        change = {
            'action': action,
            'user_agent': user_agent,
            'ip_address': ip_address,
            'timestamp': now().isoformat()
        }

        if 'changes' not in self.tab_changes:
            self.tab_changes['changes'] = []
        self.tab_changes['changes'].append(change)
        self.save()

    def count_tab_changes(self, action=None):
        """Count the number of specific tab change actions."""
        if 'changes' not in self.tab_changes:
            return 0
        if action:
            return sum(1 for change in self.tab_changes['changes'] if change['action'] == action)
        return len(self.tab_changes['changes'])

    def calculate_total_time_away(self):

        total_time_away = timedelta(0)
        last_exit_time = None

        # Loop through the changes to calculate time away
        for change in self.tab_changes.get('changes', []):
            if change['action'] in ['tab-hidden', 'mouse-left']:  # added mouse-left
                last_exit_time = now().fromisoformat(change['timestamp'])
            # added mouse-entered
            elif change['action'] in ['tab-visible', 'mouse-entered'] and last_exit_time:
                entry_time = now().fromisoformat(change['timestamp'])
                time_away = entry_time - last_exit_time
                total_time_away += time_away
                last_exit_time = None  # Reset after adding the time away

        return total_time_away


class Question(models.Model):
    text = models.CharField(max_length=1024, help_text='The text of the question')
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])

    def __str__(self):
        return self.text



class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')  # به طور فرضی از مدل User استفاده می‌کنیم
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=20)
    questions = models.ManyToManyField(Question, related_name='exams')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    def assign_random_questions(self):
        # Assign 20 random questions to the exam
        random_questions = Question.objects.order_by('?')[:self.total_questions]
        self.questions.set(random_questions)

    def calculate_score(self):
        # Calculate the score based on correct answers
        correct_answers = self.answers.filter(is_correct=True).count()
        self.score = correct_answers
        self.save()

    def __str__(self):
        return f"Exam for {self.user.phone_number} - {self.score} points"



class Answer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])

    def is_correct(self):
        return self.selected_option == self.question.correct_option

    def __str__(self):
        return f"Answer for {self.question.text}"



class QuestionBank(models.Model):
    file = models.FileField(upload_to='question_banks/', storage=FileSystemStorage(location='media/question_banks/'))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question Bank uploaded on {self.uploaded_at}"

    def save_questions_from_excel(self):
        # Load the Excel file and read its contents
        if not self.file:
            return
        
        # Use pandas to read the Excel file
        df = pd.read_excel(self.file.path)

        # Iterate through the rows in the file and save questions to the database
        for index, row in df.iterrows():
            question_text = row.get('question')
            option_a = row.get('option_a')
            option_b = row.get('option_b')
            option_c = row.get('option_c')
            option_d = row.get('option_d')
            correct_option = row.get('correct_option')

            # Create a Question object for each row in the file
            Question.objects.create(
                text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option
            )