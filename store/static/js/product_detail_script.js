toastr.options.positionClass = 'toast-bottom-right';

$('a.buy_button').click(function(e){

    let instance_id = this.getAttribute('data-instance');

    $.ajax({
        url: "/cart/add",
        data: {
            id: instance_id,
            qty: 1
        },
        success: function(result){
            toastr.success(result)
            console.log('success');
        },
        error: function(error){
            toastr.error("Cannot connect to server")
            console.log('Error');
        }
    });

});