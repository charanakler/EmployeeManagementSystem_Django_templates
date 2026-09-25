from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import DepartmentForm
from .models import Department


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    context_object_name = 'departments'
    template_name = 'departments/department_list.html'

    def get_queryset(self):
        return Department.objects.annotate(employee_total=Count('employees'))


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = 'departments/department_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = self.object.employees.all()
        return context


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('departments:department_list')

    def form_valid(self, form):
        messages.success(self.request, 'Department added successfully.')
        return super().form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Department updated successfully.')
        return reverse_lazy('departments:department_detail', kwargs={'pk': self.object.pk})


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    context_object_name = 'department'
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('departments:department_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_count'] = self.object.employees.count()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.employees.exists():
            messages.error(request, 'This department cannot be deleted while employees are assigned to it.')
            return redirect('departments:department_detail', pk=self.object.pk)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Department deleted successfully.')
        return super().form_valid(form)
