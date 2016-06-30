$(document).ready(function() {
Materialize.updateTextFields();
var button = $('#mybutton');
var frm= $('#myform');
button.click(function(event){
    event.preventDefault();
    $.ajax({url:"/polls/signedin/",type:"POST", data:frm.serialize(),
                success: function(data) {
                    if(data['success']) {
                        console.log("success")
                        window.location.replace(data['success']);
                    }
                    else if (data['failiure']) {
                        console.log("failing")
                        for (var key in data['failiure']) {
                            console.log(data['failiure'][key]);
                            $('[name="'+key+'"]').addClass('invalid');
                            id=$('[name="'+key+'"]').attr('id');
                            $('[for="'+id+'"]').attr('data-error',data['failiure'][key]);

                            //$('[name="'+key+'"]').attr("data-error",data['failiure'][key]);
                        }
                    }    
                } 
});
});
});


