from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseGenericSetting, BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.admin.panels import TabbedInterface, ObjectList

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

# Create your models here.
@register_setting
class AdminSiteSettings(BaseGenericSetting):
    admin_site_name = models.CharField(max_length=100, null=True, blank=True, help_text='Your website name')
    admin_site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        help_text='Admin logo',
        on_delete=models.CASCADE,
        related_name='+'
    )

    first_tab_panels = [
        FieldPanel('admin_site_name'),
    ]
    second_tab_panels = [
        FieldPanel('admin_site_logo'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(first_tab_panels, heading='First tab'),
        ObjectList(second_tab_panels, heading='Second tab')
    ])

    class Meta:
        verbose_name = 'Admin Site Settings'

@register_setting
class SocialMediaSettings(BaseSiteSetting):
    instagram = models.URLField(max_length=100, default='www.instagram.com/', null=True, blank=True, help_text='Instagram URL')
    facebook = models.URLField(max_length=100, default='www.facebook.com/', null=True, blank=True, help_text='Facebook URL')
    twitter = models.URLField(max_length=100, default='www.twitter.com/', null=True, blank=True, help_text='Twitter URL')
    pinterest = models.URLField(max_length=100, default='www.pinterest.com/', null=True, blank=True, help_text='Pinterest URL')
    linkedin = models.URLField(max_length=100, default='www.linkedin.com/', null=True, blank=True, help_text='Linkedin URL')
    whatsapp = models.CharField(max_length=100, default='Enter your WhatsApp number', null=True, blank=True, help_text='Whatsapp Number')
    
    panels = [
        MultiFieldPanel([
            
            FieldPanel('instagram'),
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('pinterest'),
            FieldPanel('linkedin'),
            FieldPanel('whatsapp'),
        ], heading="Social Media")
        ]

    class Meta:
        verbose_name = 'Social Media Channel'


@register_setting
class SiteSettings(BaseSiteSetting):
    site_name = models.CharField(max_length=100, null=True, blank=True, help_text='Your website name')
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        help_text='Your website logo',
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, null=True, max_length=250)
    show_in_menu_bar = models.BooleanField(default=False, blank=True, help_text='Select to show logo in menu bar', verbose_name='Menu Logo',)
    show_title_in_menu_bar = models.BooleanField(default=False, blank=True, help_text='Select to show Title in menu bar', verbose_name='Menu Title',)
    links = models.TextField(blank=True, null=True, verbose_name='Links', help_text="Use this to add links, scripts such as google analytics to the head section of the website")

    
    
    panels = [
        MultiFieldPanel([
            FieldPanel('site_name'),
            FieldPanel('show_title_in_menu_bar'),
            ]),
        
        MultiFieldPanel([
            FieldPanel('site_logo'),
            FieldPanel('show_in_menu_bar'),
            FieldPanel('caption'),
        ], heading="Website Image"),


        MultiFieldPanel([
            FieldPanel('links'),
            ], heading='Add links'),

        ]

    class Meta:
        verbose_name = 'Site Setting'

