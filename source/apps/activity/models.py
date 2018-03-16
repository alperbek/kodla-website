# Third-Party
from adminsortable.models import SortableMixin
from geoposition.fields import GeopositionField
from adminsortable.fields import SortableForeignKey

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Django
from core.models import DateModel


class Activity(DateModel):
    # Base
    year = models.PositiveSmallIntegerField(verbose_name=_('Year'), unique=True)
    is_active = models.BooleanField(verbose_name=_('Active'))
    email = models.EmailField(verbose_name=_('Email'), null=True, blank=True)

    # Features
    has_speaker_application = models.BooleanField(
        verbose_name=_('Speaker Application'), default=False
    )
    has_register = models.BooleanField(verbose_name=_('Register'), default=False)
    has_comment = models.BooleanField(verbose_name=_('Comment'), default=False)

    # Extra
    meta_tags = models.TextField(
        verbose_name=_('Meta Tags'), null=True, blank=True
    )
    logo = models.TextField(
        verbose_name=_('Logo'), null=True, blank=True
    )
    short_description = models.CharField(
        verbose_name=_('Short Description'),
        max_length=500, null=True, blank=True
    )
    description = models.TextField(
        verbose_name=_('Description'), null=True, blank=True
    )
    contact_info = models.TextField(
        verbose_name=_('Contact Information'), null=True, blank=True
    )
    register_info = models.TextField(
        verbose_name=_('Register Information'), null=True, blank=True
    )
    register_url = models.URLField(
        verbose_name=_('Register URL'), null=True, blank=True
    )
    has_register_url = models.BooleanField(
        verbose_name=_('Register URL'), default=True
    )
    has_activity_document = models.BooleanField(
        verbose_name=_('Activity Document'), default=True
    )

    # Transportation
    address = models.TextField(
        verbose_name=_('Address'), null=True, blank=True
    )
    transportation = models.TextField(
        verbose_name=_('Transportation'), null=True, blank=True
    )
    accommodation = models.TextField(
        verbose_name=_('Accommodation'), null=True, blank=True
    )

    # Speaker
    speakers = models.ManyToManyField(
        verbose_name=_('Speakers'), to='speaker.Speaker', blank=True
    )

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = ('-year',)

    def __str__(self):
        return "{year}".format(year=self.year)

    def show_register_url(self):
        if self.register_url:
            return "<a href='%s' target='_blank'>%s</a>" % (
                self.register_url, self.register_url
            )

        return self.register_url
    show_register_url.allow_tags = True
    show_register_url.short_description = _('Register URL')


def set_activity_documents_upload_path(instance, filename):
    return '/'.join([
        'activities', 'activity_%d' % instance.activity.id,
        'sponsor_docs', filename
    ])


class ActivityDocument(DateModel):
    document = models.FileField(
        verbose_name=_('Document'), upload_to=set_activity_documents_upload_path
    )
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    activity = models.ForeignKey(
        verbose_name=_('Activity'), to='activity.Activity'
    )

    class Meta:
        verbose_name = _('Activity Document')
        verbose_name_plural = _('Activity Documents')

    def __str__(self):
        return '{activity} - {document}'.format(
            activity=self.activity.__str__(), document=self.get_document_name()
        )

    def get_document_name(self):
        return str(self.document.file).split('/')[-1]

    def get_size(self):
        return self.document._get_size()

    get_size.short_description =  _('Size')

    def get_size_humanize(self):
        num = self.get_size()
        for unit in ['B','KB','MB','GB','TB','PB','EB','ZB']:
            if abs(num) < 1024.0:
                return '%3.1f%s' % (num, unit)

            num /= 1024.0
        return '%.1f%s%s' % (num, 'Y')

    get_size_humanize.short_description =  _('Size(Humanize)')

    def download_document_link(self):
        if self.document:
            return "<a href='%s' download>%s</a>" % (
                self.document.url, self.get_document_name()
            )
        else:
            return _('Document not found!')
    download_document_link.allow_tags = True
    download_document_link.short_description = _('Download')

    def show_document_link(self):
        if self.document:
            return "<a href='%s' target='_blank'>%s</a>" % (
                self.document.url, self.get_document_name()
            )
        else:
            return _('Document not found!')
    show_document_link.allow_tags = True
    show_document_link.short_description = _('Show')


class ActivitySocialAccount(DateModel, SortableMixin):
    url = models.URLField(verbose_name=_('URL'))
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    activity = models.ForeignKey(
        verbose_name=_('Activity'), to='activity.Activity'
    )
    account = models.ForeignKey(
        verbose_name=_('Account'), to='core.SocialAccount'
    )

    # ordering field
    order_id = models.PositiveSmallIntegerField(
        default=0, editable=False, db_index=True
    )

    class Meta:
        verbose_name = _('Activity Social Account')
        verbose_name_plural = _('Activity Social Accounts')
        ordering = ('order_id', 'activity')
        unique_together = ('activity', 'account')

    def __str__(self):
        return '{activity} - {account}'.format(
            activity=self.activity.__str__(), account=self.account.__str__()
        )


class ActivitySponsor(DateModel, SortableMixin):
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    logo_height = models.PositiveSmallIntegerField(
        verbose_name=_('Logo Height'), null=True, blank=True
    )
    logo_width = models.PositiveSmallIntegerField(
        verbose_name=_('Logo Width'), null=True, blank=True
    )
    sponsor_type = SortableForeignKey(
        verbose_name=_('Sponsor Type'), to='sponsor.SponsorType'
    )
    sponsor = models.ForeignKey(verbose_name=_('Sponsor'), to='sponsor.Sponsor')
    activity = models.ForeignKey(
        verbose_name=_('Activity'), to='activity.Activity'
    )

    # ordering field
    order_id = models.PositiveSmallIntegerField(
        default=0, editable=False, db_index=True
    )

    class Meta:
        verbose_name = _('Activity Sponsor')
        verbose_name_plural = _('Activity Sponsors')
        ordering = ('order_id', 'sponsor_type')
        unique_together = ('activity', 'sponsor')

    def __str__(self):
        return '{activity} - {sponsor}'.format(
            activity=self.activity.__str__(), sponsor=self.sponsor.__str__()
        )


class ActivityMap(DateModel):
    description = models.CharField(
        verbose_name=_('Description'), max_length=250, null=True, blank=True
    )
    coordinates = GeopositionField(verbose_name=_('Coordinates'))
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    activity = models.ForeignKey(
        verbose_name=_('Activity'), to='activity.Activity'
    )

    class Meta:
        verbose_name = _('Activity Map')
        verbose_name_plural = _('Activity Maps')
        ordering = ('activity',)

    def __str__(self):
        return '{activity} - {description}'.format(
            activity=self.activity.__str__(), description=self.description
        ).strip('-')
