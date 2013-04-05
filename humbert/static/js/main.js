$(document).ready(function(){

    csrf_token = $('#csrf_token').val()

    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                console.log(getCookie('csrftoken'));
            }
        } 
    });


    console.log("mountaineer to base camp");
    $('.input').focus();
    
    //for selecting input types
    choose_url = function(){
        $('#url').addClass('selected');
        $('#text').removeClass('selected');

        //make url input visible
        $('input.input').css('display', 'block');
        $('textarea.input').css('display', 'none');
        
    }

    choose_text = function(){
        $('#url').removeClass('selected');
        $('#text').addClass('selected');

        //make url input visible
        $('input.input').css('display', 'none');
        $('textarea.input').css('display', 'block');
     
    }

    $('#url').click(function(){
        choose_url();
    });

    $('#text').click(function(){
        choose_text();
    });

    create_annotation = function(){
        url = $('input.input').val();
        text = $('textarea.input').val();
        console.log(csrf_token)
        data = {
            'url':url,
            'text':text
        };
        $.post("/ajax/create_annotation", data);

    }

    $('aside').mouseup(function(e){
        e.stopPropagation();
    });

/*    $(document).mouseup(function(){
        
   var t = '';
    if(window.getSelection){
        t = window.getSelection().toString();
    }else if(document.getSelection){
        t = document.getSelection().text;
    }else if(document.selection){
        t = document.selection.createRange().text;
    }
//        console.log(t); 
        alert(t);
  
  
        

    }); */





    var timeout;
    var last_span = false;
    var HIGHLIGHT_COLOR = 'red';


    //sets a new last_span and percolates the highlight accordingly
    expand_highlight = function(new_span){
        if (last_span == false){
            last_span = parseInt(new_span.attr('id'));
            return;
        }



        new_last_span = parseInt(new_span.attr('id'));
        console.log('new last_span' + new_span.attr('id'));
        

        //needs to highlight all of the spans between the old last span and the newest last span
        for (var id=parseInt(last_span); id <= new_last_span; id++){
            $('#' + id).addClass('highlighted');
        }
        
        console.log('new last span is' + new_last_span);
        last_span = new_last_span;
    };

    minimize_highlight = function(new_span){
        if (last_span == false){
            last_span = parseInt(new_span.attr('id'));
            return;
        }

        new_last_span = parseInt(new_span.attr('id'));
        
        //iterate through
        for (var id=new_last_span; id <= parseInt(last_span); id++){
            $('#' + id).removeClass('highlighted');
        }
        last_span = new_last_span;
    }


    //makes sure that any other annotations are cleared away before starting a new one
    clean_up = function(){
        $('span.highlighted').removeClass('highlighted');
        last_span = false;
    }

    $('#annotation').bind('mousedown', function(e){
        

        e.preventDefault();
        clean_up();
        
        timeout = setInterval(function(){ 
            $('span').hover(function(){
                $(this).addClass('highlighted');
                if (parseInt($(this).attr('id')) > last_span){
                    expand_highlight($(this));
                }

                if(parseInt($(this).attr('id')) < last_span){
                    minimize_highlight($(this));
                }
            });

            
        }, 50);

    });

    $(document).bind('mouseup', function(e){
        e.preventDefault();
        console.log('mouseup');
        clearInterval(timeout);
        $('span').unbind();

    });




/*    $('#create_annotation').click(function(){
        create_annotation();
    });*/

   //i think that getting selection is probably a bad idea after all. You might as well just use mousedown and keep a tally onthe spans.


});





