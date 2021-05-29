
$(".bt-remove-product").on("click", function () {
    var product_id = $(this).val();
    console.log(product_id)
    $.ajax({
        url: '/remove_product/',
        data: {
          'product_id': product_id
        },
        dataType: 'json',
        method: "POST",
        success: function (data) {
          
        }
      });
});
