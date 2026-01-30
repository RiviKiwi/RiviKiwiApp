// Когда html документ готов (прорисован)
$(document).ready(function () {
    $(document).on('click', '.delete-btn', function(e) {
        e.preventDefault();
        
        const reviewID = $(this).data('review-id');
        const deleteUrl = $(this).data('url');
        const reviewCard = $(this).closest('.review-card');

        $.ajax({
            type: 'POST',
            url: deleteUrl,
            data: {
                review_id: reviewID,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response) {
                // Показываем уведомление об успехе
                const notification = $('#jq-notification');
                notification.html(response.message);
                notification.fadeIn(400);
                
                setTimeout(function() {
                    notification.fadeOut(400);
                }, 5000);

                // Плавно удаляем карточку отзыва
                reviewCard.fadeOut(400, function() {
                    $(this).remove();
                    
                });
            },
            error: function(response) {
                console.error('Ошибка при удалении отзыва');
            }
        });
    });

});