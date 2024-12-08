from django.db import models
from django.utils.timezone import now
from datetime import timedelta
import os
from datetime import datetime
from accounts.models import User

class TabChange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    tab_changes = models.JSONField(default=dict) 
    last_warning_time = models.DateTimeField(null=True, blank=True)
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
            elif change['action'] in ['tab-visible', 'mouse-entered'] and last_exit_time:  # added mouse-entered
                entry_time = now().fromisoformat(change['timestamp'])
                time_away = entry_time - last_exit_time
                total_time_away += time_away
                last_exit_time = None  # Reset after adding the time away

        return total_time_away


def audio_file_path(instance, filename):
    """Generate file path for new audio file with date-time based name."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # YYYYMMDD_HHMMSS
    ext = filename.split('.')[-1]  
    filename = f"{timestamp}.{ext}"  
    return os.path.join('audio', str(instance.user.phone_number), filename)  

class AudioRecording(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audio_recordings')
    file = models.FileField(upload_to=audio_file_path)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording by {self.user.phone_number} at {self.created_at}"