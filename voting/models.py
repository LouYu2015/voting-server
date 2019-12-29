from django.db import models


class Question(models.Model):
    enable = models.BooleanField("Question enabled", default=False)
    message = models.CharField(max_length=255, null=False)
    min_num_chosen = models.IntegerField("Minimum choices that must be chosen", default=1, null=False)
    max_num_chosen = models.IntegerField("Maximum choices that must be chosen", default=1, null=False)

    def __str__(self):
        return self.message


class Choice(models.Model):
    message = models.CharField(max_length=255, null=False)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class SerialNumber(models.Model):
    serial_number = models.CharField(max_length=64, null=False)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.serial_number


class Vote(models.Model):
    serial_number = models.ForeignKey(SerialNumber, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
