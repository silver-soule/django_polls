$(document).ready(function() {
var button = $('#mybutton');
var frm= $('#myform');
button.click(function(event){
    event.preventDefault();
    $.ajax({url:"/polls/loggedin/",type:"POST", data:frm.serialize(),
                success: function(data) {
                    if(data['success']) {
                        console.log("success")
                        window.location.replace(data['success']);
                    }
                    else if (data['failiure']) {
                        console.log("failing")
                        for (var key in data['failiure']) {
                            console.log([key]);
                            $('[name="'+key+'"]').addClass('invalid');
                            id=$('[name="'+key+'"]').attr('id');
                            console.log(id);
                            $('[for="'+id+'"]').attr('data-error',data['failiure'][key]);

                            
                        }
                    }

                    else if (data['invalid data']) {
                            $("#wrong_user").html(data['invalid data']);
                            $("#username").addClass('invalid');
                            $("#password").addClass('invalid');    
                    }    
                } 
});
});
});