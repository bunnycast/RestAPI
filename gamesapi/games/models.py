from django.db import models


class GameCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Game(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        related_name='games',
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)
    release_date = models.DateTimeField(auto_now_add=True)
    game_category = models.ForeignKey(
        GameCategory,
        on_delete=models.CASCADE,
        related_name='games'
    )  # using ForeignKey
    played = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):      # 각 모델 class의 제목을 무엇으로 할지 반환
        return self.name


class Player(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=True, default='', unique=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class PlayerScore(models.Model):
    player = models.ForeignKey(
        Player,
        related_name='scores',
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    score = models.IntegerField()
    score_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-score',)
