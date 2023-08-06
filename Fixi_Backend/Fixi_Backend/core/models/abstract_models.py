from model_utils.models import TimeStampedModel, SoftDeletableModel


#



class AbstractBaseModel(TimeStampedModel, SoftDeletableModel):
    class Meta:
        abstract = True
