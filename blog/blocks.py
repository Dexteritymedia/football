from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.functional import cached_property

from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    FieldBlock,
    ListBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    StructValue,
    URLBlock,
)
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks

class LinkStructValue(StructValue):
    @cached_property
    def url(self):
        if page := self.get("page"):
            return page.get_url()
        elif link_url := self.get("link_url"):
            return link_url

    @cached_property
    def text(self):
        if link_text := self.get("link_text"):
            return link_text
        elif page := self.get("page"):
            return page.title

class ImageBlock(blocks.StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False)
    attribution = blocks.CharBlock(required=False)
    shadow = blocks.ChoiceBlock(choices=[
        ('', 'Add Shadow'),
        ('S', 'Small Shadow'),
        ('R', 'Regular Shadow'),
        ('L', 'Larger Shadow')
    ], blank=True, required=False)
    
    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"
        label = "Image"


class HeadingBlock(blocks.StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = blocks.CharBlock(classname="title", required=True)
    size = blocks.ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
        label = "Heading"


class BlockQuote(blocks.StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = blocks.TextBlock()
    attribute_name = blocks.CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"
        label = "Block Quote"


class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")


    class Meta:
        template = "blocks/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class RichtextBlock(blocks.RichTextBlock):

    def get_api_representation(self, value, context=None):
        return richtext(value.source)


    class Meta:
        template = "blocks/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"



class SimpleRichtextBlock(blocks.RichTextBlock):

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = ['bold','italic','link']


    class Meta:
        template = "blocks/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"



class CTABlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=['bold','italic'])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Read More', max_length=40)


    class Meta:
        template = "blocks/cta_block.html"
        icon = "plus"
        label = "Call to Action"

class ButtonBlock(blocks.StructBlock):
    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')


    class Meta:
        template = "blocks/button_block.html"
        icon = "link"
        label = "Single Button"
        value_class = LinkStructValue


class DragAndDropTableBlock(blocks.StructBlock):
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('name', blocks.CharBlock(required=True, max_length=40)),
            ]),
        label="Table Items",
        )

    class Meta:
        template = ""

    def render(self, value, context=None):
        items = value['items']
        return mark_safe(f'''
            <table id="drag-table" class="table">
                <!-- Add your table structure here -->
                <!-- Example rows: -->
                <tr data-id="1"><td>Item 1</td></tr>
                <tr data-id="2"><td>Item 2</td></tr>
                <tr data-id="3"><td>Item 3</td></tr>
            </table>
            <input type="hidden" name="{name}" id="sorted-ids" value="">
        ''')

    class Media:
        js = ('sortable.js', 'admin/js/drag_and_drop_table.js')


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=True)),
                ('title', blocks.CharBlock(required=True, max_length=40)),
                ('text', blocks.TextBlock(required=True, max_length=200)),
                ('button_page', blocks.PageChooserBlock(required=False)),
                ('button_url', blocks.URLBlock(required=False, help_text='If the button page above is selected, that will be used first')),
            ]
        )
    )


    class Meta:
        template = "blocks/card_block.html"
        icon = "list-ul"
        label = "Cards"


class JumbotronBlock(blocks.StructBlock):

    jumbotron = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=False)),
                ('subtitle', blocks.CharBlock(required=False, max_length=40)),
                ('body', blocks.RichTextBlock(required=True, features=['h1','h2','h3','h4','h5','h6','hr','bold','italic','link'],)),
                ('color', blocks.CharBlock(required=False, max_length=40, help_text="Enter a hexdecimal color for the background e.g #000000")),
                ('button_page', blocks.PageChooserBlock(required=False)),
                ('button_url', blocks.URLBlock(required=False, help_text='If the button page above is selected, that will be used first')),
            ]
        )
    )


    class Meta:
        template = "blocks/jumbotron_block.html"
        icon = "list-ul"
        label = "Jumbotron"
        max_num = 1


class JumbotronBlockWithTextColor(blocks.StructBlock):

    jumbotron = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=False)),
                ('title', blocks.CharBlock(required=False, max_length=40)),
                ('description', blocks.RichTextBlock(required=False, features=['h1','h2','h3','h4','h5','h6','hr','bold','italic','link','code','superscript','subscript','strikethrough','blockquote',],)),
                ('color', blocks.CharBlock(required=False, max_length=40, help_text="Enter a hexdecimal color for the background e.g #000000")),
                ('text_color', blocks.CharBlock(required=False, max_length=40, help_text="Enter a hexdecimal color for the text e.g #000000 or red")),
            ]
        )
    )


    class Meta:
        template = "blocks/jumbotron_text_block.html"
        icon = "list-ul"
        label = "Jumbotron"
        max_num = 1


class InternalLinkBlock(StructBlock):
    page = PageChooserBlock()
    link_text = CharBlock(required=False)

    class Meta:
        label = "Internal link"
        icon = "link"
        value_class = LinkStructValue


class ExternalLinkBlock(StructBlock):
    link_url = URLBlock(label="URL")
    link_text = CharBlock()

    class Meta:
        label = "External link"
        icon = "link"
        value_class = LinkStructValue


class LinkBlock(StreamBlock):
    internal_link = InternalLinkBlock()
    external_link = ExternalLinkBlock()

    class Meta:
        label = "Link"
        icon = "link"
        max_num = 1


class KeyPoint(StructBlock):
    title = CharBlock()
    intro = CharBlock()
    link = PageChooserBlock()

    class Meta:
        icon = "form"


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(
        choices=(
            ("left", "Wrap left"),
            ("right", "Wrap right"),
            ("half", "Half width"),
            ("full", "Full width"),
        )
    )


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    alignment = ImageFormatChoiceBlock()
    caption = CharBlock()
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"


class ImageWithLinkBlock(StructBlock):
    image = ImageChooserBlock()
    link = LinkBlock(required=False)

    class Meta:
        icon = "site"


class PhotoGridBlock(StructBlock):
    images = ListBlock(ImageChooserBlock())

    class Meta:
        icon = "grip"


class PullQuoteBlock(StructBlock):
    quote = CharBlock(form_classname="quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class PullQuoteImageBlock(StructBlock):
    quote = CharBlock()
    attribution = CharBlock()
    image = ImageChooserBlock(required=False)


class TestimonialBlock(StructBlock):
    quote = CharBlock(form_classname="quote title")
    name = CharBlock()
    role = CharBlock()
    link = LinkBlock(required=False)

    class Meta:
        icon = "openquote"


class BustoutBlock(StructBlock):
    image = ImageChooserBlock()
    text = RichTextBlock()

    class Meta:
        icon = "pick"


class WideImage(StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "image"


class StatsBlock(StructBlock):
    pass

    class Meta:
        icon = "order"


class EmbedPlusCTABlock(StructBlock):
    title = CharBlock()
    intro = CharBlock()
    link = PageChooserBlock(required=False)
    external_link = URLBlock(label="External Link", required=False)
    button_text = CharBlock()
    image = ImageChooserBlock(required=False)
    embed = EmbedBlock(required=False, label="Youtube Embed")

    def clean(self, value):
        struct_value = super().clean(value)

        errors = {}
        image = value.get("image")
        embed = value.get("embed")

        if image and embed:
            error = ErrorList(
                [
                    ValidationError(
                        "Either an image or a Youtube embed may be specified, but not both."
                    )
                ]
            )
            errors["image"] = errors["embed"] = error

        if errors:
            raise StructBlockValidationError(errors)
        return struct_value


class CTABlock(StructBlock):
    text = CharBlock(
        help_text="Words in  &lt;span&gt; tag will display in a contrasting colour."
    )
    link = LinkBlock()


class StoryBlock(StreamBlock):
    h2 = CharBlock(
        form_classname="title",
        icon="title",
        template="blocks/streamfield/heading2_block.html",
    )
    h3 = CharBlock(
        form_classname="title",
        icon="title",
        template="blocks/streamfield/heading3_block.html",
    )
    h4 = CharBlock(
        form_classname="title",
        icon="title",
        template="blocks/streamfield/heading4_block.html",
    )
    intro = RichTextBlock(
        icon="pilcrow",
        template="blocks/streamfield/intro_block.html",
    )
    paragraph = RichTextBlock(
        icon="pilcrow",
        template="blocks/streamfield/paragraph_block.html",
    )
    aligned_image = ImageBlock(
        label="Aligned image",
        template="blocks/streamfield/aligned_image_block.html",
    )
    wide_image = WideImage(
        label="Wide image",
        template="blocks/streamfield/wide_image_block.html",
    )
    bustout = BustoutBlock(
        template="blocks/streamfield/bustout_block.html"
    )
    pullquote = PullQuoteBlock(
        template="blocks/streamfield/pullquote_block.html"
    )
    raw_html = RawHTMLBlock(
        label="Raw HTML",
        icon="code",
        template="blocks/streamfield/raw_html_block.html",
    )
    mailchimp_form = RawHTMLBlock(
        label="Mailchimp embedded form",
        icon="code",
        template="blocks/streamfield/mailchimp_form_block.html",
    )
    embed = EmbedBlock(
        icon="code",
        template="blocks/streamfield/embed_block.html",
        group="Media",
    )

    class Meta:
        template = "blocks/streamfield/stream_block.html"


class PageSectionStoryBlock(StreamBlock):
    key_points_summary = ListBlock(
        KeyPoint(),
        icon="list-ul",
        min_num=4,
        max_num=6,
        template="blocks/streamfield/key_points_summary.html",
        help_text="Please add a minumum of 4 and a maximum of 6 key points.",
    )
    testimonials = ListBlock(
        TestimonialBlock(),
        icon="openquote",
        template="blocks/streamfield/testimonial_block.html",
    )
    clients = ListBlock(
        ImageWithLinkBlock(),
        icon="site",
        template="blocks/streamfield/client-logo-block.html",
        label="Clients logo",
    )
    embed_plus_cta = EmbedPlusCTABlock(
        label="Embed + CTA",
        icon="code",
        template="blocks/streamfield/embed_plus_cta_block.html",
    )
    cta = CTABlock(
        icon="plus-inverse",
        template="blocks/streamfield/cta.html",
    )

    class Meta:
        template = "blocks/stream_block.html"
