$(document).ready(function(){
    
    //starts highlighting mode
    start_highlighting = function(){
        alert('yooo');
        isHighlighting = true;
        $('html').addClass('isHighlighting');
        $("aside").css('display', 'none');
        $('#compose_screen').css('display', 'block');
    }

    //ends highlighting mode
    stop_highlighting = function(){
        isHighlighting = false;
        $('html').removeClass('isHighlighting');
        $("aside").css('display', 'block');
        $('#compose_screen').css('display', 'none');
        clean_up();
    }

    //save comment
    save_comment = function(){
        comment = $('#post_note').val();
        post_comment(start, last_span, comment);
        stop_highlighting();
    }

    post_comment = function(begin, end, comment){
        //ajax call to make the comment
       
        //display comment 
        display_comment(begin, end, comment);
    }

    display_comment = function(begin, end, comment){
        //display published_highlight
        for(var i=begin; i<=end; i++){
            $('#' + i).addClass('published_highlight');
        }

        //this will be like a priority queue in terms of location.
        //we move it left of the start point and below every note (which should have a 10px bottom padding)   
    }

    $('#annotate_button').click(function(){
        start_highlighting();
    });

    $('button#discard').click(function(){
        stop_highlighting();
    });

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

    var highlighted_text='';

    set_highlighted_text = function(){
        text ='';

        if (start==false){
            $('#highlighted_text').text(text);
        }

        else if(start < last_span){
            for (var i = start; i <= last_span; i++){
                text += $('#' + i).text() + ' ';
            }
            $('#highlighted_text').text(text);
        }
        
        else if(start > last_span){
            for (var i = last_span; i <= start; i++){
                text += $('#' + i).text() + ' ';
            }
            $('#highlighted_text').text(text);
        }
        
        else {
            $('#highlighted_text').text($('#' + start).text());
            
        }

        
    }


    var timeout;
    var last_span = false;
    var start = false;
    var HIGHLIGHT_COLOR = '#064780';
    var min_span;
    var isHighlighting = false;
    
    //expands in positive direction or minimizes in negative direction
    expand_highlight = function(current_id){

        percolate_highlight(parseInt(last_span), current_id);

        //continuous disintegration
        if(current_id >= last_span && current_id < start){
            disintegrate_highlight(min_span, current_id -1);
        }

        //discontinuous disintegration for cases where we have jumps past the start point.
        if(current_id > start){
            disintegrate_highlight(min_span, start -1);
        }
        
        last_span = current_id;
        min_span = Math.min(min_span, last_span);
    };

    //minimizes in positive direction or expands in negative direction
    minimize_highlight = function(current_id){
        disintegrate_highlight(current_id, last_span);
        
        if (start > current_id){
            percolate_highlight(current_id, start);
        }

        last_span = current_id;
        min_span = Math.min(min_span, last_span);
    }


////////////////HIGHLIGHT ADDITION/SUBTRACTION
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
//////////////////////////////////////////////

    //makes sure that any other annotations are cleared away before starting a new one
    clean_up = function(){
        $('span.highlighted').removeClass('highlighted');
        last_span = false;
        start = false;
        min_span = false;
        set_highlighted_text();
    }

    $('#annotation').bind('mousedown', function(e){
        if(!isHighlighting){
            return;
        }
        e.preventDefault();

        clean_up();
        
        timeout = setInterval(function(){ 
            $('span').hover(function(e){
                current_id = parseInt($(this).attr('id'));
                
                if (start==false){
                    start = current_id;
                    min_span = start;
                    last_span = start;
                    expand_highlight(current_id);
                }


                e.stopPropagation();
                $(this).addClass('highlighted');

                if (current_id > last_span){
                    expand_highlight(current_id);
                }

                if(current_id < last_span){
                    minimize_highlight(current_id);
                }

                set_highlighted_text();
            });
            
        }, 25);

    });

    $(document).bind('mouseup', function(e){
        e.preventDefault();
        clearInterval(timeout);
        $('span').unbind();
        return false;
    });


    $('aside').mouseup(function(){
        //stop propagation
        $('#annotation').trigger('mouseup');
        clearInterval(timeout);
        return false;
    });

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


