from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):            # ✅ M + V ធំ
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

