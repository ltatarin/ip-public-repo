$(function() {  
    $('.saveFavourite').click(function() {
        let comment = prompt('Ingrese un comentario para la imagen: ');

        if (comment !== null) {
            $(this).closest('form').find('.comment').val(comment);
            $(this).closest('form').submit();
        }
    });
});