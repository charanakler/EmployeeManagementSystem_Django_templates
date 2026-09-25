from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from departments.models import Department

from .forms import EmployeeForm
from .models import Employee


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employees/employee_list.html'
    paginate_by = 10

    def get_queryset(self):
        employees = Employee.objects.select_related('department')
        search_term = self.request.GET.get('q', '').strip()
        department_id = self.request.GET.get('department', '').strip()
        status = self.request.GET.get('status', '').strip()
        designation = self.request.GET.get('designation', '').strip()

        if search_term:
            employees = employees.filter(
                Q(employee_id__icontains=search_term)
                | Q(first_name__icontains=search_term)
                | Q(last_name__icontains=search_term)
                | Q(email__icontains=search_term)
            )
        if department_id.isdigit():
            employees = employees.filter(department_id=department_id)
        if status in Employee.Status.values:
            employees = employees.filter(status=status)
        if designation:
            employees = employees.filter(designation=designation)
        return employees

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['designations'] = (
            Employee.objects.exclude(designation='')
            .order_by('designation')
            .values_list('designation', flat=True)
            .distinct()
        )
        context['selected_department'] = self.request.GET.get('department', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_designation'] = self.request.GET.get('designation', '')
        context['search_term'] = self.request.GET.get('q', '')
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employees/employee_detail.html'

    def get_queryset(self):
        return Employee.objects.select_related('department')


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')

    def form_valid(self, form):
        messages.success(self.request, 'Employee added successfully.')
        return super().form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Employee updated successfully.')
        return reverse_lazy('employees:employee_detail', kwargs={'pk': self.object.pk})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employees:employee_list')

    def form_valid(self, form):
        messages.success(self.request, 'Employee deleted successfully.')
        return super().form_valid(form)
