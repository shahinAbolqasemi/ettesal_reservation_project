from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """
    This model is An Custom User model
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def check_group(self, group_name):
        if self.groups.filter(name=group_name).exists():
            return True
        else:
            return False

    def check_any_groups(self, groups_name):
        if self.groups.filter(name__in=groups_name).exists():
            return True
        else:
            return False


class BaseModel(models.Model):
    """
    This Model is AbstractModel that base model for other model
    """

    class Meta:
        abstract = True

    created_time = models.DateTimeField(verbose_name=_('created time'), auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name=_('modified time'), auto_now=True)
    related_creator = models.ForeignKey(
        verbose_name=_('creator'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_creator_related',
        related_query_name='%(class)s_creator'
    )


class SessionRequest(BaseModel):
    nodes_count = models.PositiveIntegerField(verbose_name=_('nodes count'))
    groups_count = models.PositiveIntegerField(verbose_name=_('group count'))
    unique_id = models.CharField(verbose_name=_('unique id'), max_length=5, unique=True)
    related_customer = models.ForeignKey(
        verbose_name=_('customer'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_customer_related',
        related_query_name='%(class)s_customer'
    )
    is_accepted = models.BooleanField(verbose_name=_('is accepted'), default=False)
    start_date = models.DateTimeField(verbose_name=_('start date'))
    end_date = models.DateTimeField(verbose_name=_('end date'))
    related_participants = models.ManyToManyField(
        verbose_name=_('participants'),
        to='Participant',
        through='ParticipantAssignment',
        through_fields=('related_session_request', 'related_participant'),
        related_name='%(class)s_participants_related',
        related_query_name='%(class)s_participants'
    )


class Participant(BaseModel):
    title = models.CharField(verbose_name=_('title'), max_length=200, unique=True)

    class Meta:
        verbose_name = _('participant')
        verbose_name_plural = _('participants')


class ParticipantAssignment(BaseModel):
    related_session_request = models.ForeignKey(
        verbose_name=_('session request'),
        to='SessionRequest',
        on_delete=models.PROTECT,
        related_name='%(class)s_session_request_related',
        related_query_name='%(class)s_session_request'
    )
    related_participant = models.ForeignKey(
        verbose_name=_('participant request'),
        to='Participant',
        on_delete=models.PROTECT,
        related_name='%(class)s_participant_related',
        related_query_name='%(class)s_participant'
    )

    class Meta:
        verbose_name = _('participant assignment')
        verbose_name_plural = _('participant assignments')
        constraints = [
            models.UniqueConstraint(
                fields=('related_session_request', 'related_participant'),
                name='unique_session_participant'
            ),
        ]
