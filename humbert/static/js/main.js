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
    var start = false;
    var HIGHLIGHT_COLOR = 'red';

    //sets a new last_span and percolates the highlight accordingly
    expand_highlight = function(current_id){
        if (last_span == false){
            last_span = current_id;
            return;
        }
        
        percolate_highlight(parseInt(last_span), current_id);
        last_span = current_id;
    };

    minimize_highlight = function(current_id){
        if (last_span == false){
            last_span = current_id;
            return;
        }

        //iterate through
        disintegrate_highlight(current_id, last_span);
        
        if (start > current_id){
            percolate_highlight(current_id, start);
        }

        last_span = current_id;
    }

    percolate_highlight = function(min, max){
        //This function will create a highlight between to spans.          
        for (var id=parseInt(min); id <= parseInt(max); id++){
            $('#' + id).addClass('highlighted');
        }
    }

    disintegrate_highlight = function(min, max){
        for (var id=min; id <=max; id++){
            $('#' + id).removeClass('highlighted');
        }
    }


    //makes sure that any other annotations are cleared away before starting a new one
    clean_up = function(){
        $('span.highlighted').removeClass('highlighted');
        last_span = false;
        start = false;
    }

    $('#annotation').bind('mousedown', function(e){
        e.preventDefault();

        clean_up();
        
        console.log("start");

        timeout = setInterval(function(){ 
            $('span').hover(function(e){
                current_id = parseInt($(this).attr('id'));

                if (start==false){
                    start = current_id;
                }

                e.stopPropagation();
                $(this).addClass('highlighted');
                if (current_id > last_span){
                    expand_highlight(current_id);
                }

                if(current_id < last_span){
                    minimize_highlight(current_id);
                }
            });
            
        }, 25);

    });

    $(document).bind('mouseup', function(e){
        e.preventDefault();
        console.log('mouseup');
        clearInterval(timeout);
        $('span').unbind();
        return false;
    });

    $(document).mousedown(function(e){
        e.preventDefault();
    });


/*    $('#create_annotation').click(function(){
        create_annotation();
    });*/

   //i think that getting selection is probably a bad idea after all. You might as well just use mousedown and keep a tally onthe spans.


});












