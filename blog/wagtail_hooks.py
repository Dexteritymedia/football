from wagtail import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import BlogIndexPage, BlogDetailPage, BlogListingPage, BlogTagPage

#to change the name "Snippets" to Overview in wagtail admin sidebar
@hooks.register('construct_main_menu')
def change_page_name(request, menu_items):
    for item in menu_items:
        if item.__class__.__name__=='SnippetsMenuItem':
            item.label = 'Snippets'

#hide the help page from main menu
@hooks.register("construct_main_menu")
def hide_help_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "help"]

#hide the explorer/pages/overview page from main menu
"""
@hooks.register("construct_main_menu")
def hide_help_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "explorer"]
"""

#hide the locked page from reports submenu
@hooks.register("construct_reports_menu")
def hide_help_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "locked-pages"]

#hide the sites page from settings submenu
@hooks.register("construct_settings_menu")
def hide_help_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "sites"]

#hide the redirect page from settings submenu
@hooks.register("construct_settings_menu")
def hide_help_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "redirects"]
    
#to change the name "Pages" to Overview in wagtail admin sidebar
@hooks.register('construct_main_menu')
def change_page_name(request, menu_items):
    for item in menu_items:
        if item.__class__.__name__=='ExplorerMenuItem':
            item.label = 'Overview'

class HomePageAdmin(ModelAdmin):
    model = BlogIndexPage
    menu_label = 'Homepage'
    menu_icon = 'home'
    menu_order = 150
    add_to_settings_menu = False
    exclude_from_explorer = False

class BlogListingPageAdmin(ModelAdmin):
    model = BlogListingPage
    menu_label = 'Blog'
    menu_icon = 'plus-inverse'
    menu_order = 160
    add_to_settings_menu = False
    exclude_from_explorer = False

class BlogDetailPageAdmin(ModelAdmin):
    model = BlogDetailPage
    menu_label = 'Blog posts'
    menu_order = 170
    menu_icon = 'doc-empty-inverse'
    list_display = ('title', 'slug', 'latest_revision_created_at')
    list_filter = ('title', 'latest_revision_created_at')
    search_fields = ('title', 'body', 'latest_revision_created_at')


class BlogTagPageAdmin(ModelAdmin):
    model = BlogTagPage
    menu_label = 'Tags'
    menu_order = 190
    menu_icon = 'pilcrow'
    list_display = ('title', 'slug', 'latest_revision_created_at')
    list_filter = ('title', 'latest_revision_created_at')
    search_fields = ('title', 'body', 'latest_revision_created_at')


modeladmin_register(HomePageAdmin)
modeladmin_register(BlogListingPageAdmin)
modeladmin_register(BlogDetailPageAdmin)
modeladmin_register(BlogTagPageAdmin)
