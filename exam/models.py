from django.db import models
from django.utils.timezone import now
from datetime import timedelta
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
            elif change['action'] in ['tab-visible', 'mouse-entered'] and last_exit_time:  # added mouse-entered
                entry_time = now().fromisoformat(change['timestamp'])
                time_away = entry_time - last_exit_time
                total_time_away += time_away
                last_exit_time = None  # Reset after adding the time away

        return total_time_away