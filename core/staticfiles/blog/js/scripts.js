$(document).ready(function () {


 
    $("#id_email").keyup(function(){
      var email=$(this).val();

     if(email!=""){
          $.ajax({
              url:"/dashboard/check_email_exist/",
              type:'POST',
              data:{email:email},
              success: function(response){
                console.log(response)
                var filter = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
                  if(response=="True"){
                      $(".email_error").remove();
                      $("<span class='email_error' style='padding: 5px;color: red;font-weight: bold;'>Email already exists.Please, use another email.</span>").insertAfter("#email_msg");
                  }
                  else if(filter.test(email)){//for email 
                    $(".email_error").remove();
                    $("<span class='email_error' style='padding: 5px;color: green;font-weight: bold;'></span>").insertAfter("#id_email");
                }
                 
                 
              }
              ,
              error: function(){
                console.log("failed")
              }
           
          })
         
      }
      else{
        $(".email_error").remove();
      }

  });

});