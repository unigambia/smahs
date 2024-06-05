from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.students.models import Student

from .forms import InvoiceItemFormset, InvoiceReceiptFormSet, Invoices
from .models import Invoice, InvoiceItem, Receipt


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice


class InvoiceCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Invoice
    fields = "__all__"
    success_url = "/finance/list"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["items"] = InvoiceItemFormset(
                self.request.POST, prefix="invoiceitem_set"
            )
        else:
            context["items"] = InvoiceItemFormset(prefix="invoiceitem_set")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["items"]
        self.object = form.save()
        if self.object.id != None:
            if form.is_valid() and formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super().form_valid(form)
    
    def get_form(self):
        """add date picker in forms"""
        form = super(InvoiceCreateView, self).get_form()
        form.fields.pop("created_by")
        form.fields.pop("updated_by")
        return form


class InvoiceDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Invoice
    fields = "__all__"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context["receipts"] = Receipt.objects.filter(invoice=self.object)
        context["items"] = InvoiceItem.objects.filter(invoice=self.object)
        return context


class InvoiceUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = ["student", "session", "term", "class_for", "balance_from_previous_term"]

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["receipts"] = InvoiceReceiptFormSet(
                self.request.POST, instance=self.object
            )
            context["items"] = InvoiceItemFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["receipts"] = InvoiceReceiptFormSet(instance=self.object)
            context["items"] = InvoiceItemFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["receipts"]
        itemsformset = context["items"]
        if form.is_valid() and formset.is_valid() and itemsformset.is_valid():
            form.save()
            formset.save()
            itemsformset.save()
        return super().form_valid(form)


class InvoiceDeleteView(UserPassesTestMixin, SuccessMessageMixin ,LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice-list")
    success_message = "Invoice was deleted successfully"


class ReceiptCreateView(UserPassesTestMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")
    success_message = "Receipt was created successfully"

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        obj.invoice = invoice
        obj.save()
        return redirect("invoice-list")

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET["invoice"])
        context["invoice"] = invoice
        return context


class ReceiptUpdateView(UserPassesTestMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Receipt
    fields = ["amount_paid", "date_paid", "comment"]
    success_url = reverse_lazy("invoice-list")
    success_message = "Receipt was updated successfully"

    def test_func(self):
        return self.request.user.is_superuser
    
class ClearanceListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "finance/clearance_list.html"
    context_object_name = "students"
    queryset = Student.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ClearanceListView, self).get_context_data(**kwargs)
        context["students"] = Student.objects.filter(is_cleared=False)
        return context
    
class ClearanceUpdateView(UserPassesTestMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Student
    fields = ["is_cleared"]
    success_url = reverse_lazy("clearance-list")
    success_message = "Student has been cleared successfully"

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(ClearanceUpdateView, self).get_context_data(**kwargs)
        student = Student.objects.get(pk=self.request.GET["student"])
        context["student"] = student
        return context

class ReceiptDeleteView(UserPassesTestMixin, SuccessMessageMixin ,LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy("invoice-list")
    success_message = "Receipt was deleted successfully"

    def test_func(self):
        return self.request.user.is_superuser


@login_required
@user_passes_test(lambda u: u.is_superuser)
def bulk_invoice(request):
    return render(request, "finance/bulk_invoice.html")
