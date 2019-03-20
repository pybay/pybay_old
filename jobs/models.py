from django.db import models

from ordered_model.models import OrderedModel

ORDERING_CHOICES = [(3500, 'Platinum'), (2000, 'Diamond'), (1500, 'Gold'), (1000, 'Silver'), (500, 'Bronze'), (0, 'None')]

class VisibleJobManager(models.Manager):
    def get_queryset(self):
        return super(VisibleJobManager, self).get_queryset().filter(display=True)
    def all(self):
      return super(VisibleJobManager, self).all().order_by('-level', 'order')

class Job(OrderedModel):
    class Meta:
        verbose_name = 'Job Details'
        verbose_name_plural = 'Job Postings'

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, default="", help_text="Employer name.")
    contact_email = models.EmailField(max_length=255,
                                      help_text="Not shared publicly. Be sure to use the email"
                                                " associated with your Paypal account.",
                                      default="")
    contact_phone = models.CharField(max_length=20, help_text="Not shared publicly.", default="")
    display = models.BooleanField(help_text="Show this job posting on the site.", default=False)
    logo = models.ImageField(upload_to="logos", blank=True)
    url = models.SlugField(help_text="Give the posting a short slug to be used in the url")
    details = models.TextField("Summary", help_text="Short and punchy text")
    lengthy_details = models.TextField("Details", blank=True, help_text="The rest of the details. Use markdown for bulleted lists, *italics*, etc.")
    link = models.CharField(max_length=255, default="", help_text="Add a link to apply for this job.")
    level = models.IntegerField(choices=ORDERING_CHOICES, default=0)
    location = models.CharField(max_length=100, default="")

    def get_absolute_url(self):
      return "/jobs/%s/" % self.url

    def __unicode__(self):
        return self.title



    objects = models.Manager()
    visible = VisibleJobManager()
