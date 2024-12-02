from django.contrib import admin
from .models import TabChange, Question, Exam, Answer


# تنظیمات نمایش TabChange در پنل ادمین
@admin.register(TabChange)
class TabChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('tab_changes',)


# تنظیمات نمایش Question در پنل ادمین
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam', 'correct_option')
    list_filter = ('exam',)
    search_fields = ('text',)
    list_per_page = 20


# تنظیمات نمایش Exam در پنل ادمین
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'total_questions', 'started_at', 'finished_at')
    list_filter = ('started_at', 'finished_at')
    search_fields = ('name',)
    readonly_fields = ('started_at', 'score')
    fieldsets = (
        (None, {
            'fields': ('name', 'question_file', 'total_questions')  # افزودن 'name'
        }),
        ('Timestamps', {
            'fields': ('finished_at',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Ensure questions are extracted from Excel file when saving an Exam
        super().save_model(request, obj, form, change)
        if not change and obj.question_file:
            obj.save_questions_from_excel()


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('exam', 'user', 'question', 'selected_option', 'is_correct')  # اضافه کردن user به نمایش
    list_filter = ('exam', 'user')  # امکان فیلتر کردن بر اساس کاربر
    search_fields = ('question__text', 'user__username', 'user__email')

    def is_correct(self, obj):
        return obj.is_correct()
    is_correct.boolean = True
    is_correct.short_description = 'Correct Answer'

