from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.corecode.current_user import get_current_user

from .models import Invoice, InvoiceItem, Receipt


@receiver(post_save, sender=Invoice)
def after_creating_invoice(sender, instance, created, **kwargs):
    if created:
        previous_inv = (
            Invoice.objects.filter(student=instance.student)
            .exclude(id=instance.id)
            .last()
        )
        if previous_inv:
            previous_inv.status = "closed"
            previous_inv.save()
            instance.balance_from_previous_term = previous_inv.balance()
            instance.save()


@receiver(pre_save, sender=Invoice)
def invoice_pre_save(sender, instance, **kwargs):
    # This signal runs before a Invoice is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()


@receiver(pre_save, sender=InvoiceItem)
def invoice_item_pre_save(sender, instance, **kwargs):
    # This signal runs before a InvoiceItem is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()


@receiver(pre_save, sender=Receipt)
def receipt_pre_save(sender, instance, **kwargs):
    # This signal runs before a Receipt is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()


