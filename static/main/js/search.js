$(document).ready(function() {
    $('#searchForm').submit(function(e) {
        e.preventDefault();
        var query = $('#searchInput').val();

        $.ajax({
            url: 'search/', // Замените на URL вашего представления search
            data: {
                'q': query
            },
            success: function(data) {
                $('#searchResults').html(data);
            }
        });
    });
});

success: function(data) {
    console.log(data); // Отображение данных в консоли браузера
    $('#searchResults').html(data);
}