$(document).ready(function() {
    $("#home").click(function() {
        $('html, body').animate({scrollTop:'0%'}, 800);
    });
});
$(document).ready(function() {
    $("#menu0").click(function() {
        $('html, body').animate({scrollTop:'0%' }, 800);
    });
});
$(document).ready(function(){
    $(function(){ $('#menu1').click(function(){ 
        $('html,body').animate({scrollTop:$('#hr01').offset().top}, 800);});  
    }); 
}); 
$(document).ready(function(){
    $(function(){ $('#menu2').click(function(){ 
        $('html,body').animate({scrollTop:$('#hr02').offset().top}, 800);});  
    }); 
}); 
$(document).ready(function(){
    $(function(){ $('#menu3').click(function(){ 
        $('html,body').animate({scrollTop:$('#hr03').offset().top}, 800);});  
    }); 
}); 
$(document).ready(function(){
    $(function(){ $('#action-1').click(function(){ 
        $('html,body').animate({scrollTop:$('#hr03').offset().top}, 800);});  
    }); 
});
$(document).ready(function(){
    $(function(){ $('#action-2').click(function(){ 
        $('html,body').animate({scrollTop:$('#hr03').offset().top}, 800);});  
    }); 
});
$(document).ready(function(){
    $(function(){ $('#action-3').click(function(){ 
        $('html,body').animate({scrollTop:$('#hr03').offset().top}, 800);});  
    }); 
});
$(document).ready(function(){
    $(function(){ $('#menu4').click(function(){ 
        $('html,body').animate({scrollTop:$('#hr04').offset().top}, 800);});  
    }); 
});
$(window).load(function(){
            $(".col-3 input").val("");
            
            $(".input-effect input").focusout(function(){
                if($(this).val() != ""){
                    $(this).addClass("has-content");
                }else{
                    $(this).removeClass("has-content");
                }
            })
        });