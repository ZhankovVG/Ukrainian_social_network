$(document).ready(function () {
    $(".like-button").on("click", function () {
        var post_id = $(this).data("post-id");
        var like_button = $(this);

        $.ajax({
            type: "POST",
            url: "{% url 'newsfeed:like_post' %}",
            data: {
                'post_id': post_id,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function (data) {
                if ('likes' in data) {
                    $("#likes_count_" + post_id).text(data.likes);
                }
            },
            error: function (data) {
                console.log('Error:', data);
            }
        });
    });
});