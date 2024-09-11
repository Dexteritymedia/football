from django import forms
from django.utils.safestring import mark_safe

class DragAndDropTableWidget(forms.Widget):
    template_name = 'admin/widgets/drag_and_drop_table.html'

    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f'''
            <table id="drag-table" class="table">
                <!-- Add your table structure here -->
                <!-- Example rows: -->
                <tr data-id="1"><td>Item 1</td></tr>
                <tr data-id="2"><td>Item 2</td></tr>
                <tr data-id="3"><td>Item 3</td></tr>
            </table>
            <input type="hidden" name="{name}" id="sorted-ids" value="{value}">
        ''')

    class Media:
        js = ('sortable.js', 'admin/js/drag_and_drop_table.js')
