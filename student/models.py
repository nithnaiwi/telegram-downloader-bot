from django.db import models
import datetime  # ត្រូវ import datetime ដើម្បីប្រើសម្រាប់ default នៃ DateField


class Student(models.Model):
    name = models.CharField(max_length=100)

    # Fields ពី Model ទី១
    age = models.IntegerField(null=True, blank=True)  # ធ្វើឱ្យ null/blank ដើម្បីឱ្យទិន្នន័យចាស់អាចគ្មាន age
    grade = models.CharField(max_length=10, null=True, blank=True)  # ធ្វើឱ្យ null/blank

    # Fields ពី Model ទី២
    gender = models.CharField(max_length=10, null=True, blank=True)  # អាចឱ្យ null/blank ប្រសិនបើទិន្នន័យចាស់មិនមាន

    # សម្រាប់ birth_date យើងដាក់ default មួយ ឬ null=True, blank=True
    # ឧទាហរណ៍: ខ្ញុំជ្រើសរើសដាក់ default មួយ
    birth_date = models.DateField(default=datetime.date(2000, 1, 1))  # កំណត់ថ្ងៃខែឆ្នាំកំណើត default
    # ជម្រើសផ្សេង: birth_date = models.DateField(null=True, blank=True)

    gmail = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    # សម្រាប់ branch យើងដាក់ default មួយ ឬ null=True, blank=True
    # ឧទាហរណ៍: ខ្ញុំជ្រើសរើសដាក់ default មួយ
    branch = models.CharField(max_length=100, default=' Phnom Penh Branch')  # កំណត់ឈ្មោះសាខា default
    # ជម្រើសផ្សេង: branch = models.CharField(max_length=100, null=True, blank=True)

    major = models.CharField(max_length=100, null=True, blank=True)
    degree_level = models.CharField(max_length=50, null=True, blank=True)
    study_time = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name