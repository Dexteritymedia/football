from django.db import models

# Create your models here.
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel )
from wagtail.search import index
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.snippets.models import register_snippet
#from wagtail.snippets.panels import SnippetChooserPanel

from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager

#from wagtail.admin.edit_handlers import TabbedInterface, ObjectList

from . import blocks

from .blocks import PageSectionStoryBlock, StoryBlock
from .widgets import DragAndDropTableWidget

class MyDraggableTablePage(Page):
    sorted_ids = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('sorted_ids', widget=DragAndDropTableWidget),
    ]


class BlogIndexPage(Page):
    page_description = "Use this page to create a sports blog"
    max_count = 1
    template = 'blog/blog.html'
    subpage_types = [
        'blog.BlogDetailPage',
        'blog.BlogListingPage',
        'blog.BlogTagPage',
        #'sportsblog.Service',
        ]
    show_in_menus_default = True


    def get_context(self, request):
        context = super().get_context(request)
        top_three_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')[0:2]#First four
        top_four_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')[2:4]
        #featured_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')[6:12]
        topics = BlogListingPage.objects.live().public().order_by('-first_published_at')
        #all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')[12:]
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        print(top_three_posts)
        categories = BlogListingPage.objects.live().public()[:5]#first five categories


        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])
        

        paginator = Paginator(all_posts, 25)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['top_three_posts'] = top_three_posts
        context['top_four_posts'] = top_four_posts
        #context['featured_posts'] = featured_posts
        context['topics'] = topics
        context['categories'] = categories
        return context


    class Meta:
        verbose_name = 'Sports blog'
        verbose_name_plural = 'Sports blog'


class BlogListingPage(Page):
    page_description = "Use this page to add categories to the blog"
    template = "blog/blog_listing_page.html"

    subpage_types = ['blog.BlogDetailPage']
    parent_page_types = [
        'blog.BlogIndexPage'
        ]
    show_in_menus_default = True

    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        )


    heading = StreamField(
        [
            
            ('jumbotron', blocks.JumbotronBlockWithTextColor()),
            ('full_richtext', blocks.RichtextBlock()),
            ('image', blocks.ImageBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        MultiFieldPanel([
            FieldPanel('heading'),
            ], heading='Additional Information'),
    ]


    class Meta:
        verbose_name = 'Sports Blog Category'
        verbose_name_plural = 'Sports Blog Categories'



    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = BlogListingPage.get_children(self,).live().order_by('-first_published_at')
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])
        

        paginator = Paginator(blogpages, 20)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()
        return context




class BlogDetailPage(Page):
    page_description = "Use this page to create a blog post"
    template = 'blog/blog_detail.html'
    subpage_types = [
        'blog.BlogDetailPage',
    ]
    parent_page_types = [
        'blog.BlogIndexPage', 'blog.BlogListingPage'
    ]
    
    date = models.DateTimeField(default=timezone.now, verbose_name='Date')
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        )
    call_to_action = StreamField(
        PageSectionStoryBlock(),
        blank=True,
        use_json_field=True,
        collapsed=True,
        null=True,
    )
    body = StreamField(StoryBlock(), use_json_field=True, null=True)
    tags = ClusterTaggableManager(through="blog.BlogPostPageTag", blank=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    listing_summary = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True, max_length=255)
    related_services = ParentalManyToManyField(
        "blog.Service", related_name="blog_posts", blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('image'),
        FieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("call_to_action"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel("feed_image"),
        FieldPanel("listing_summary"),
        FieldPanel("canonical_url"),
        FieldPanel("related_services", widget=forms.CheckboxSelectMultiple),
    ]


    settings_panels = [
        FieldPanel('subtitle'),
        InlinePanel('blog_categories', label="category", max_num=1),
    ]
        
    
    class Meta:
        verbose_name = 'Sports Blog Post'
        verbose_name_plural = 'Sports Blog Posts'

    def get_context(self, request):
        context = super().get_context(request)
        entries = BlogDetailPage.objects.live().public().exclude(id=self.id).order_by('-first_published_at')[:4]
        #previous_post = BlogDetailPage.objects.live().public().filter(id__gt=self.id).order_by('id').only('id').first().id
        #next_post = BlogDetailPage.objects.live().public().filter(id__lt=self.id).order_by('id').only('id').first().id
        #print(previous_post)
        #print(next_post)
        #context['previous_post'] = previous_post
        #context['next_post'] = next_post
        context['entries'] = entries
        return context


class BlogTagPage(Page):
    page_description = "Use this page to create a homepage for tags"
    template = "blog/blog_tag.html"
    max_count = 1
    parent_page_types = [
        'blog.BlogIndexPage'
        ]
    subpage_types = [
        'blog.BlogTagPage'
        ]

    description = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        print(tag)
        blogpages = BlogDetailPage.objects.filter(tags__name=tag)
        print(blogpages)
        # Update template context
        context = super().get_context(request)
        paginator = Paginator(blogpages, 2)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['blogpages'] = blogpages
        return context

    class Meta:
        verbose_name = "Blog Tag"

        
@register_snippet
class SportsTag(TaggitTag):
    class Meta:
        proxy = True


class BlogPostPageTag(TaggedItemBase):
    content_object = ParentalKey("blog.BlogDetailPage", related_name="post_tags")


class BlogCategory(models.Model):
    page = ParentalKey('blog.BlogDetailPage', on_delete=models.CASCADE, related_name='blog_categories')
    blog_category = models.ForeignKey(
        'blog.BlogCategory', on_delete=models.CASCADE, related_name='blog_pages')

    panels = [
        FieldPanel('blog_category'),
        ]

    class Meta:
        unique_together = ('page', 'blog_category')


class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["sort_order"]

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("sort_order"),
    ]
