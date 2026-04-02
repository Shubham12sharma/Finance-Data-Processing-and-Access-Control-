from django.db import models
from django.utils import timezone
from users.models import User

class FinancialRecord(models.Model):
    """Financial transaction or entry model"""
    
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    
    CATEGORY_CHOICES = (
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('health', 'Health'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='financial_records'
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Transaction amount"
    )
    record_type = models.CharField(
        max_length=10, 
        choices=TYPE_CHOICES
    )
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES
    )
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    
    # Soft delete support (good practice)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Financial Record'
        verbose_name_plural = 'Financial Records'

    def __str__(self):
        return f"{self.record_type.capitalize()} - ₹{self.amount} ({self.category}) by {self.user.username}"

    def soft_delete(self):
        self.is_deleted = True
        self.save()