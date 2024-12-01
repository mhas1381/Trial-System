from django.contrib import admin
from django.utils.safestring import mark_safe
import json
from .models import *


class TabChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at', 'formatted_tab_changes')
    readonly_fields = ('formatted_tab_changes',)  

    def formatted_tab_changes(self, obj):
        try:
            formatted_json = json.dumps(obj.tab_changes, indent=4)
            return mark_safe(f'<pre>{formatted_json}</pre>')  
        except Exception as e:
            return "Invalid JSON Format"

    formatted_tab_changes.short_description = "Tab Changes"  

admin.site.register(TabChange, TabChangeAdmin)

from django.contrib import admin


from django.contrib import admin
from .models import Question, Exam, Answer, QuestionBank

# پنل ادمین برای مدل Question
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option')
    search_fields = ('text', 'option_a', 'option_b', 'option_c', 'option_d')
    list_filter = ('correct_option',)
    ordering = ('text',)
    
admin.site.register(Question, QuestionAdmin)


# پنل ادمین برای مدل Exam
class ExamAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'total_questions', 'started_at', 'finished_at')
    search_fields = ('user__phone_number',)
    list_filter = ('started_at', 'finished_at')
    readonly_fields = ('score', 'started_at', 'finished_at')
    
    def save_model(self, request, obj, form, change):
        # هنگام ذخیره کردن آزمون، به طور خودکار سوالات تصادفی را اختصاص دهید
        obj.assign_random_questions()
        super().save_model(request, obj, form, change)
    
admin.site.register(Exam, ExamAdmin)


# پنل ادمین برای مدل Answer
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question', 'selected_option', 'is_correct')  # نمایش متد is_correct در لیست
    search_fields = ('exam__user__phone_number', 'question__text')
    list_filter = ('selected_option',)  # استفاده از فیلدهای واقعی برای فیلتر کردن
    
    # اضافه کردن یک فیلتر سفارشی برای is_correct (اگر نیاز دارید)
    def is_correct(self, obj):
        return obj.selected_option == obj.question.correct_option
    is_correct.boolean = True  # نمایش به عنوان آیکون صحیح/غلط
    
admin.site.register(Answer, AnswerAdmin)


# پنل ادمین برای مدل QuestionBank
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    search_fields = ('file',)
    
    def save_model(self, request, obj, form, change):
        # بعد از ذخیره کردن، سوالات را از فایل اکسل بارگذاری کنید
        super().save_model(request, obj, form, change)
        obj.save_questions_from_excel()
    
admin.site.register(QuestionBank, QuestionBankAdmin)
