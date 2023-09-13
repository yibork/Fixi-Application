from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from Fixi_Backend.core.models import AbstractBaseModel
from rest_framework.exceptions import NotAcceptable
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from pictures.models import PictureField


class ReviewReportReason(AbstractBaseModel):
    report_cause = models.CharField(max_length=255)
    is_other = models.BooleanField(default=False)

    def __str__(self):
        return self.report_cause

class ReviewReport(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name="reported_by")
    review = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True)
    reason = models.ForeignKey('ReviewReportReason', on_delete=models.SET_NULL, null=True)
    reason_other = models.TextField(max_length=2500, blank=True)
    message = models.TextField(max_length=2500)

    def __str__(self):
        return f"{self.user} report {self.review.id}"

class ReviewVotes(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='voter')
    review = models.ForeignKey('Review', on_delete=models.CASCADE)

class ReviewCategory(AbstractBaseModel):
    admin = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='added_by')
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class Review(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name="created_by")
    category = models.ForeignKey('ReviewCategory', on_delete=models.SET_NULL, null=True, related_name='reviews')
    votes = models.ManyToManyField('users.User', related_name='voters', blank=True, through="ReviewVotes")
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=500)
    message = models.TextField(max_length=2500)
    tags = models.ManyToManyField('ReviewTag', blank=True, related_name='reviews')  # Adjusted related_name

    @property
    def get_tags(self):
        return self.tags.all()
    def __str__(self):
        return f"{self.stars} on {self.service.name}"

    @property
    def get_media(self):
        return ReviewMedia.objects.filter(review=self)
class ReviewTag(AbstractBaseModel):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='review_tags')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='review_tags')

    def __str__(self):
        return str(self.tag)

class Tag(AbstractBaseModel):
    tags = TaggableManager(blank=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return str(self.name)

class ReviewMedia(AbstractBaseModel):
    image = PictureField(upload_to='review_images', blank=True, null=True)
    video = PictureField(upload_to='review_videos', blank=True, null=True)
    review = models.ForeignKey('Review', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)


    def __str__(self):
        return f"Media for {self.review}"
