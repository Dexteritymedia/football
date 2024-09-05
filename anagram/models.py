from django.db import models

# Create your models here.

class Letter(models.Model):
    letter = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.letter} was created on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class WordBuilding(models.Model):
    words = models.TextField()
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='word_letter',)


    def __str__(self):
        return f"{self.words} from {self.letter.letter}"
