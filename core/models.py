from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser


from django.conf import settings



class email_for_send_message(models.Model):
    email = models.EmailField(max_length=800)

    def __str__(self):
        return self.email



class Skill(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    Price = models.DecimalField(max_digits=8, decimal_places=2)
    deadline = models.DateField(auto_now_add=True)
    skills = models.ManyToManyField(Skill, related_name='jobs')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_jobs')

    def __str__(self):
        return self.title
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.urls import reverse


class Proposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    project = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='proposals')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=900)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    cover_letter = models.TextField()
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cv_file = models.FileField(upload_to='cv_files/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    


    
    def __str__(self):
        return f"Proposal for {self.project.title} by {self.name}"
    
    def get_absolute_url(self):
        return reverse('dashboard')
    

@receiver(post_save, sender=Proposal)
def send_proposal_acceptance_email(sender, instance, created, **kwargs):
    if instance.status == 'accepted':
        subject = f"You are accepted for project: {instance.project.title}"
        html_message = render_to_string('email.html', {'proposal': instance })
        plain_message = strip_tags(html_message)
        recipient_list = [instance.email]
        send_mail(subject, plain_message ,settings.FROM_EMAIL, recipient_list ,html_message=html_message)


    


    
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class Send_Projects_file(models.Model):
    FILE_STATUS_CHOICES = [
        ('Revising', 'Revising'),
        ('accepted', 'Accepted'),
        ('Solved', 'Solved'),
        ('Error and Bugs', 'Error and Bugs'),
        ('completed', 'Completed'),
    ]

    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Send_Projects_file_hires')
    project = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='jobs_Send_Projects_file')
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="Send_Projects_file_proposals")
    file_status = models.CharField(max_length=20, choices=FILE_STATUS_CHOICES, default='pending')
    file = models.FileField(upload_to="projects_file" ,  storage=RawMediaCloudinaryStorage())

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the Send_Projects_file is being created for the first time
        super().save(*args, **kwargs)

        if created:
            proposal = self.proposal
            Earning_money.objects.create(
                freelancer=self.freelancer,
                project=self.project,
                proposal=proposal,
                money=proposal.bid_amount
            )

    def __str__(self):
        return f"Sending file for {self.project.title} by {self.proposal.name} file status {self.file_status}"




class Earning_money(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Earning_freelancer')
    project = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='Earning_Projects')
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="Earning_proposals")
    money = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Earning for {self.project.title} - Freelancer: {self.freelancer.username} money {self.money} "
    
    @staticmethod
    def get_total_money_for_freelancer(freelancer):
        return Earning_money.objects.filter(freelancer=freelancer).aggregate(total_money=models.Sum('money'))['total_money']
    

class Pay_out_money(models.Model):
    DESTINATION_TYPE_CHOICES = [
        ('bkash', 'bkash Account'),
        ('paypal', 'Paypal Account'),
        ('bank', 'Bank Account'),
    ]

    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Pay_out_money_freelancer')
    earning_money = models.ForeignKey(Earning_money, on_delete=models.CASCADE, related_name='earning_money')
    project = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='Pay_out_money_Projects')
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="Pay_out_money_proposals")
    money = models.FloatField(default=0.0)
    destination_type = models.CharField(max_length=10, choices=DESTINATION_TYPE_CHOICES, default='bkash')
    destination_name = models.CharField(max_length=900, blank=True)
    destination_phone = models.CharField(max_length=900, blank=True)
    destination_address = models.CharField(max_length=900, blank=True)
    paypal_name = models.CharField(max_length=300, blank=True)
    paypal_email = models.CharField(max_length=300, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    account_holder_name = models.CharField(max_length=200, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    routing_number = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=900, default="We are sending your money to your account in 24 Hours")

    def __str__(self):
        return f"Pay out money for {self.project.title} - Freelancer: {self.freelancer.username}"



class Hire(models.Model):
    project = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='hires')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hires')
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Hire for {self.project.title} - Freelancer: {self.freelancer.username}"



class About_us(models.Model):
   name = models.CharField(max_length=300)
   RichTextField = RichTextField()
   def __str__(self):
        return self.name 


class contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=600)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name + self.email + self.subject


class service(models.Model):
    name = models.CharField(max_length=300)
    content = RichTextField()
    def __str__(self):
        return self.name 








