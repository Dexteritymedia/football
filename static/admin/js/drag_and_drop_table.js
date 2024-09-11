document.addEventListener('DOMContentLoaded', function() {
    var table = document.getElementById('drag-table');
    var input = document.getElementById('sorted-ids');

    var sortable = new Sortable(table, {
        onEnd: function (evt) {
            var rows = table.querySelectorAll('tr');
            var order = Array.from(rows).map(function(row) {
                return row.getAttribute('data-id');
            });
            input.value = order.join(',');
        }
    });
});