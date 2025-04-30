from django.db import models

class ServiceModel(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    image_alt = models.CharField(max_length=64)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def save(self, *args, **kwargs):
        if self.priority is None:
            last_priority = ServiceModel.objects.count()
            self.priority = last_priority + 1

        super(ServiceModel, self).save(*args, **kwargs)

        all_services = ServiceModel.objects.all().order_by('priority')
        for index, service in enumerate(all_services, start=1):
            if service.priority != index:
                service.priority = index
                service.save(update_fields=['priority'])

    def __str__(self):
        return f'{self.title}' 