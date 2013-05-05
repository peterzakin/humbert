$(document).ready(function(){
    var ANNOTATION_ID = $('#annotation_id').val();
    comments = window.INITIAL_COMMENTS;

    //display comments is called immediately
    display_comments();
    
    //starts highlighting mode
    start_highlighting = function(){
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

    $('#post_note').click(function(){
        if(!$.trim($('#annotation_comment').val())){
            return;
        };
        save_comment();
    });

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
        }

        $.post("/ajax/create_annotation", data);

    }

    var highlighted_text='';

    set_highlighted_text = function(){
        text ='';

        if (start===false){
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
                
                if (start===false){
                    start = current_id;
                    min_span = start;
                    last_span = start;
          //          expand_highlight(current_id);
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
            
        }, 1);

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

        //save comment does nothing to db.
    save_comment = function(){
        comment_text = $('#annotation_comment').val();
        //start and last span are globals 
//        display_published_higlight(start, last_span, comment_text);
        add_comment($("#" + start).offset().top, start, last_span, comment_text);
        stop_highlighting();
    }
    
    //save annotation sends all of the comments to db and saves annotation itself
    save_annotation = function(){
        var data = {};
        data['text_id'] = TEXT_ID;
        data['user_id'] = USER_ID;
        data['comments'] = JSON.stringify(comments);
        data['text_title'] = TEXT_TITLE;
        var response = $.post("/ajax/save_annotation", data, function(data){
            console.log(data);
            window.ANNOTATION_ID = data;

        }); 
        console.log(response);
    }

    $('#save_annotation_button').click(function(){
        if(comments.length > 0){
            save_annotation();
        }

    });
    
});

FONT_SIZE = 12;

//when we add things like profile pic etc... we'll want to add to this size.
STANDARD_PADDING_BETWEEN_COMMENTS = 48;

Comment = function(offset, first_span, last_span, text, author){
    this.offset = offset;
    this.first_span = first_span;
    this.last_span = last_span;
    this.text = text;
    this.author = author;
}

add_comment = function(offset, first_span, last_span, text){
    author = USERNAME;
    comment = new Comment(offset, first_span, last_span, text, author);
    //position comment in stack based on its offset
    position_comment_in_stack(comment);
    $('.comment').remove();
    comments.push(comment);
    comments.sort(compare_comments);
    display_comments();
}

compare_comments = function(a,b){
    if(a.first_span < b.first_span){
        return -1;
    }
    if (a.first_span > b.first_span){
        return 1;
    }

    return 0;
}

//sorts comment in stack
position_comment_in_stack = function(comment){
    console.log(comment);
    for(var p=0; p < comments.length; p++){
        console.log(p);
        sibling = comments[p]
        console.log(sibling);
        
        if(sibling.first_span == comment.first_span && sibling.last_span == comment.last_span){
            //they're the same
            continue;
        }

        else if(sibling.offset > comment.offset){
            diff = sibling.offset - comment.offset;
            if(diff < calculate_comment_height_from_length(comment.text.length)){
                sibling.offset = comment.offset + calculate_comment_height_from_length(comment.text.length); //+ STANDARD_PADDING_BETWEEN_COMMENTS;
                position_comment_in_stack(sibling);
            }
        } else if(comment.offset > sibling.offset) {
            diff = comment.offset - sibling.offset;
            if(diff < calculate_comment_height_from_length(sibling.text.length)){
                comment.offset = sibling.offset + calculate_comment_height_from_length(sibling.text.length); //+ STANDARD_PADDING_BETWEEN_COMMENTS;
                position_comment_in_stack(comment);
            }
        }

        else {
            //they have the same offset but different start and last spans
            if(comment.first_span < sibling.first_span){
                sibling.offset = comment.offset + calculate_comment_height_from_length(comment.text.length);
                position_comment_in_stack(sibling);
            } else {
                comment.offset = sibling.offset + calculate_comment_height_from_length(sibling.text.length);
                position_comment_in_stack(comment);
            }
        }

    }

    
}

var COMMENT_HEADER_SIZE = 12;
calculate_comment_height_from_length = function(comment_length){
    
    //50 is how many characters can fit in horizontal space
    //ESSENTIALLY LINES * FONTSIZE + 1 LINE FOR 
    comment_height = (Math.floor(comment_length/50) + 1) * FONT_SIZE + STANDARD_PADDING_BETWEEN_COMMENTS + COMMENT_HEADER_SIZE;
    
    console.log('height is' + comment_height);
    return comment_height;
}


    post_comment = function(start_span, end_span, comment){
        //ajax call to make the comment
        data = {
            'comment': comment,
         //   'annotation_id': ANNOTATION_ID,
            'start_span': String(start_span),
            'end_span': String(end_span)
        };

        $.post("/ajax/create_comment", data); 
    }

    display_published_higlight = function(start_span, end_span, comment){
        //display published_highlight
        for(var i=start_span; i<=end_span; i++){
            $('#' + i).addClass('published_highlight');
        }

     }



//DISPLAY COMMENTS
display_comments = function(){
    //WHAT SHOULD WE DO ABOUT COMMENTS THAT ALREADY EXIST.
    //IF THERES BEEN A CHANGE, THEN WE NEED TO REMOVE THE OLD ONES AND REFRESH    
    for(var j=0; j< comments.length; j++){
        comment = comments[j];
        author_html = "<a class='comment_author' href='/" + comment.author + "'>" + comment.author + "</a>";
        author_html += "<div class='comment_photo'><img src=" + USER_PHOTO_URL + "/></div>";
        html = "<div class='comment' style='top:" + comment.offset + "px'>" + author_html + comment.text + " </div>";
        $('aside').append(html);

        //display highlight
        console.log(comment);
        display_published_higlight(comment.first_span, comment.last_span, comment.text);
    }
}










