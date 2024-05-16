# Generated by Django 4.2.3 on 2024-05-16 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram', models.URLField(blank=True, default='www.instagram.com/', help_text='Instagram URL', max_length=100, null=True)),
                ('facebook', models.URLField(blank=True, default='www.facebook.com/', help_text='Facebook URL', max_length=100, null=True)),
                ('twitter', models.URLField(blank=True, default='www.twitter.com/', help_text='Twitter URL', max_length=100, null=True)),
                ('pinterest', models.URLField(blank=True, default='www.pinterest.com/', help_text='Pinterest URL', max_length=100, null=True)),
                ('linkedin', models.URLField(blank=True, default='www.linkedin.com/', help_text='Linkedin URL', max_length=100, null=True)),
                ('whatsapp', models.CharField(blank=True, default='Enter your WhatsApp number', help_text='Whatsapp Number', max_length=100, null=True)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Social Media Channel',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(blank=True, help_text='Your website name', max_length=100, null=True)),
                ('caption', models.CharField(blank=True, max_length=250, null=True)),
                ('show_in_menu_bar', models.BooleanField(blank=True, default=False, help_text='Select to show logo in menu bar', verbose_name='Menu Logo')),
                ('show_title_in_menu_bar', models.BooleanField(blank=True, default=False, help_text='Select to show Title in menu bar', verbose_name='Menu Title')),
                ('links', models.TextField(blank=True, help_text='Use this to add links, scripts such as google analytics to the head section of the website', null=True, verbose_name='Links')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
                ('site_logo', models.ForeignKey(blank=True, help_text='Your website logo', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Site Setting',
            },
        ),
        migrations.CreateModel(
            name='AdminSiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_site_name', models.CharField(blank=True, help_text='Your website name', max_length=100, null=True)),
                ('admin_site_logo', models.ForeignKey(blank=True, help_text='Admin logo', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Admin Site Settings',
            },
        ),
    ]
