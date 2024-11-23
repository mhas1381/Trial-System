from django.db import models
from django.utils.timezone import now
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