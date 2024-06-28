var page = 1;
var limit = 3;
var endPagination = false;
var isLoading = false;

$(function() {  
    limit = $('.imagesByPage').val();
    $('.imagesByPage').change(function() {
        limit = $(this).val();
    })

    $('.home').on('click', '.saveFavourite', function() {
        let comment = prompt('Ingrese un comentario para la imagen: ');

        if (comment !== null) {
            let form = $(this).closest('form');
            form.find('.comment').val(comment);

            let data = form.serialize();
            $.post(form.attr('action'), data, function(){
                form.find('.saveFavourite').hide();
                form.find('.isFavourite').show();
            });            
        }
    });

    if ($('.home').length) {
        $(window).scroll(function() {
            if (($(window).innerHeight() + $(window).scrollTop()) >= $('body').height()-10) {
                if (!isLoading && !endPagination) {
                    page += 1;
                    showPage(page, limit);
                }
            }
        });

        showPage(page, limit);
    }
});

function showPage(page, limit) {
    let query = $('#search').val() ? $('#search').val() : '';
    isLoading = true;
    $('.loadingSpinner').show();

    let data = {};
    if (query) {
        data = {query, csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()};
    }

    $.ajax(window.location.pathname + '?page=' + page + '&limit=' + limit, 
        {
            method: query ? 'POST' : 'GET',
            data,
            success: function(r) {
                isLoading = false;
                $('.loadingSpinner').hide();
        
                if (r.length) {
                    $(r).insertBefore('.loadingSpinner');
                } else {
                    endPagination = true;
                }
            }
        }
    );
}