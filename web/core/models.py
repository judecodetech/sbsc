from django.conf import settings
from django.utils.safestring import mark_safe

from django.db import models


class Suspect(models.Model):
    # gender choices
    MALE = 'Male'
    FEMALE = 'Female'

    # face complexion choices
    DARK = 'Dark'
    FAIR = 'Fair'
    PIMPLES = 'Pimples'
    OLIVE = 'OLIVE'
    SPOTS = 'Spots'
    PALE = 'Pale'
    SUNBURNT = 'Sunburnt'

    # # face shape choices
    ROUND = 'Round'
    ANGULAR = 'Angular'
    OVAL = 'Oval'
    LONG = 'Long'
    THIN = 'Thin'
    SQUARE = 'Square'
    FRECKLED = 'Freckled'

    # hair choices
    BLOND = 'blond'
    FAIR = 'Fair'
    RED = 'Red'
    BROWN = 'Brown'
    BLACK = 'Black'
    GREY = 'Grey'
    WHITE = 'White'
    LONG = 'Long'
    SHORT = 'Short'
    CURLY = 'Curly'
    FRIZZY = 'Frizzy'
    STRAIGHT = 'Straight'
    BALD = 'Bald'

    # cheek choices
    WIDE = 'Wide'
    CHUBBY = 'Chubby'
    PLUMP = 'Plump'
    HOLLOW = 'Hollow'
    SUNKEN = 'Sunken'
    DIMPLES = 'Dimples'
    BLUSHING = 'Blushing'
    PINK = 'Pink'

    # ear choices
    CURVING = 'Curving'
    POINTED = 'Pointed'
    FLOPPY = 'Floppy'

    # eyelashes choices
    WINGED = 'Winged'
    STRAIGHT = 'Straight'
    THIN = 'Thin'
    ARTIFICIAL = 'Artificial'
    THICK = 'Thick'
    SHORT = 'Short'
    LONG = 'Long'
    CURLING = 'Curling'

    # eyebrows choices
    BUSHY = 'Bushy'
    THICK = 'Thick'
    RAISED = 'Raised'
    PENCILLED = 'Pencilled'

    # eyes choices
    BROWN = 'Brown'
    BLACK = 'Black'
    BLUE = 'Blue'
    HAZEL = 'Hazel'
    BLOOD_SHOT = 'Blood-shot'

    # nose choices
    SMALL = 'Small'
    BIG = 'Big'
    POINTED = 'Pointed'
    
    first_name = models.CharField(
        max_length=50, 
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=50, 
        blank=False,
        null=False,
    )

    image = models.ImageField(
        blank=False,
    )

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(
        max_length=7, 
        choices=GENDER_CHOICES,
        blank=False
    )

    FACE_COMPLEXION_CHOICES = (
        (DARK, 'dark'),
        (FAIR, 'fair'),
        (PIMPLES, 'pimples'),
        (OLIVE, 'olive'),
        (SPOTS, 'spots'),
        (PALE, 'pale'),
        (SUNBURNT, 'sunburnt'),
    )
    face_complexion = models.CharField(
        max_length=15,
        choices=FACE_COMPLEXION_CHOICES,
    )

    FACE_SHAPE_CHOICES = (
        (ROUND, 'round'),
        (ANGULAR, 'angular'),
        (OVAL, 'oval'),
        (LONG, 'long'),
        (THIN, 'thin'),
        (SQUARE, 'square'),
        (FRECKLED, 'freckled'),
    )
    face_shape = models.CharField(
        max_length=15,
        choices=FACE_SHAPE_CHOICES,
    )

    HAIR_CHOICES = (
        (BLACK, 'black'),
        (BLOND, 'blonde'),
        (FAIR, 'fair'),
        (RED, 'red'),
        (BROWN, 'brown'),
        (GREY, 'grey'),
        (WHITE, 'white'),
        (LONG, 'long'),
        (SHORT, 'short'),
        (CURLY, 'curly'),
        (STRAIGHT, 'straight'),
        (BALD, 'bald'),
    )

    hair = models.CharField(
        max_length=15,
        choices=HAIR_CHOICES,
    )

    CHEEK_CHOICES = (
        (CHUBBY, 'chubby'),
        (WIDE, 'wide'),
        (PLUMP, 'pimples'),
        (HOLLOW, 'hollow'),
        (SUNKEN, 'sunken'),
        (DIMPLES, 'dimples'),
        (BLUSHING, 'blushing'),
        (PINK, 'pink'),
    )
    cheek = models.CharField(
        max_length=15,
        choices=CHEEK_CHOICES,
    )

    EAR_CHOICES = (
        (CURVING, 'curving'),
        (POINTED, 'pointed'),
        (FLOPPY, 'floppy'),
    )
    ear = models.CharField(
        max_length=15,
        choices=EAR_CHOICES,
    )

    EYELASHES_CHOICES = (
        (SHORT, 'short'),
        (WINGED, 'winged'),
        (STRAIGHT, 'straight'),
        (THIN, 'thin'),
        (ARTIFICIAL, 'artificial'),
        (THICK, 'thick'),
        (LONG, 'long'),
        (CURLING, 'curling'),
    )
    eyelashes = models.CharField(
        max_length=15,
        choices=EYELASHES_CHOICES,
    )

    EYEBROW_CHOICES = (
        (BUSHY, 'bushy'),
        (THICK, 'thick'),
        (RAISED, 'raised'),
        (PENCILLED, 'pencilled'),
    )
    eyebrow = models.CharField(
        max_length=15,
        choices=EYEBROW_CHOICES,
    )

    EYES_CHOICES = (
        (BROWN, 'brown'),
        (BLACK, 'black'),
        (BLUE, 'blue'),
        (HAZEL, 'hazel'),
        (BLOOD_SHOT, 'blood-shot'),
    )
    eyes = models.CharField(
        max_length=15,
        choices=EYES_CHOICES,
        default=BROWN,
    )

    NOSE_CHOICES = (
        (SMALL, 'small'),
        (BIG, 'big'),
        (POINTED, 'pointed'),
    )
    nose = models.CharField(
        max_length=15,
        choices=NOSE_CHOICES,
    )

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name

    def image_tag(self):
        return mark_safe('<img src="{}" />').format(self.image.url)

    image_tag.short_description = 'Avatar'
    image_tag.allow_tags = True
