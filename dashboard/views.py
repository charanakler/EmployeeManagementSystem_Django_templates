from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from departments.models import Department
from employees.models import Employee


@login_required
def dashboard_view(request):
    employees = Employee.objects.select_related('department')
    context = {
        'total_employees': employees.count(),
        'active_employees': employees.filter(status=Employee.Status.ACTIVE).count(),
        'inactive_employees': employees.filter(status=Employee.Status.INACTIVE).count(),
        'total_departments': Department.objects.count(),
        'recent_employees': employees[:5],
    }
    return render(request, 'dashboard/dashboard.html', context)
