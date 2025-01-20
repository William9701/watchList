from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.db.models import Avg


class User(AbstractUser):
    favorites = models.ManyToManyField("Show", blank=True, related_name="favorited_by")
    def __str__(self):
        return self.username

class Show(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the show
    title = models.TextField()  # The title of the show
    genre = models.TextField() # The genre the show belongs to
    description = models.TextField() # The description of the show
    rating = models.ManyToManyField(User, through='Rating', related_name='rated_shows')

    favorites = models.ManyToManyField(User, related_name='liked_shows', blank=True)  # Users who favorited the show
    image_url = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.title}"
    
    def update_average_rating(self):
        average = self.ratings.aggregate(Avg('stars'))['stars__avg'] or 0
        self.average_rating = round(average, 2)
        self.save()
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_show = models.ForeignKey(Show, related_name='ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'rated_show')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the Review
    show = models.ForeignKey(Show, on_delete=models.CASCADE)  # The show the Review belongs to
    text = models.TextField()  # The Review text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the Review was created

    def __str__(self):
        return f"Review by {self.user.username} on {self.show.title}"
