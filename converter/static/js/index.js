'use strict';
    
// create an alert div
var createAlert = function(alert_type){
    // if alert already exists, remove current alert
    if(!!document.getElementById("alert")){
        var delete_alert = document.getElementById("alert");
        delete_alert.parentNode.removeChild(delete_alert);
    }

    var new_alert = document.createElement('div');
    new_alert.className = "alert alert-dismissible fade show nonselect";
    new_alert.className += " alert-"+alert_type;
    new_alert.id = "alert";
    new_alert.setAttribute("role", "alert");

    var alert_message = document.createElement('div');
    alert_message.id = "alert_message";

    var close_button = document.createElement('button');
    close_button.id = "close_button";
    close_button.classList.add("close");
    close_button.setAttribute("data-dismiss", "alert");
    close_button.setAttribute("aria-label", "Close");
    
    var close_sign = document.createElement('span');
    close_sign.setAttribute("aria-hidden", "true");
    close_sign.innerHTML = "&times;"

    document.getElementById('alert_box').appendChild(new_alert);
    document.getElementById('alert').appendChild(alert_message);
    document.getElementById('alert').appendChild(close_button);
    document.getElementById('close_button').appendChild(close_sign);
};

// feature detection for drag&drop upload
var isAdvancedUpload = function()
    {
        var div = document.createElement( 'div' );
        return ( ( 'draggable' in div ) || ( 'ondragstart' in div && 'ondrop' in div ) ) && 'FormData' in window && 'FileReader' in window;
    }();

// applying the effect for every form
var forms = document.querySelectorAll( '.box' );
var text_form = document.getElementById('text_input');

function textSubmit(e) {
    var form_data = new FormData();
        form_data.append('text', document.getElementById("textcontent").value);
        form_data.append('format', document.getElementById("textformat").value);
        $.ajax({
            type: 'POST',
            url: '/convert_result/submission',
            data: form_data,
            contentType: false,
            processData: false,
            success: function(data) {
                var result_data = JSON.parse(data);
                if(result_data.is_success){
                    var result_text = result_data.result;
                    document.title = "Result Page";
                    document.getElementById('the_title').innerHTML = "Result";
                    $('#main_page').slideUp(500);
                    $('#result_page').slideDown(1500);     
                    createAlert('success');               
                }
                else{
                    createAlert('danger');
                }
                document.getElementById('alert_message').innerHTML = result_data.message;
                document.getElementById('alert').style.display = 'block';
                $('#text').slideUp(500);
            },
            error: function(data){
                window.location.href = '/';                
                document.getElementById('alert_message').innerHTML = "An unknown error occurred";
                document.getElementById('alert').style.display = 'block';
            }
        });
        e.preventDefault();
}

text_form.addEventListener('submit', textSubmit);

var upload_file = false;
Array.prototype.forEach.call( forms, function( form )
{
    var input		 = form.querySelector( 'input[type="file"]' ),
        label		 = form.querySelector( 'label' ),
        showFiles	 = function( files )
        {
            label.textContent = files[ 0 ].name;
        }

    // automatically submit the form on file select
    input.addEventListener( 'change', function( e )
    {   
        upload_file = e.target.files
        showFiles( upload_file );
    });

    // drag&drop files if the feature is available
    if( isAdvancedUpload )
    {
        form.classList.add( 'has-advanced-upload' ); // letting the CSS part to know drag&drop is supported by the browser

        [ 'drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop' ].forEach( function( event )
        {
            form.addEventListener( event, function( e )
            {
                // preventing the unwanted behaviours
                e.preventDefault();
                e.stopPropagation();
            });
        });
        [ 'dragover', 'dragenter' ].forEach( function( event )
        {
            form.addEventListener( event, function()
            {
                form.classList.add( 'is-dragover' );
            });
        });
        [ 'dragleave', 'dragend', 'drop' ].forEach( function( event )
        {
            form.addEventListener( event, function()
            {
                form.classList.remove( 'is-dragover' );
            });
        });
        form.addEventListener( 'drop', function( e )
        {
            upload_file = e.dataTransfer.files; // the files that were dropped
            showFiles( upload_file );                    
        });
    }

    // if the form was submitted
    form.addEventListener( 'submit', function( e )
    {
        var form_data = new FormData();
        form_data.append('file', upload_file[0]);
        $.ajax({
            type: 'POST',
            url: '/convert_result/upload',
            data: form_data,
            contentType: false,
            processData: false,
            success: function(data) {
                var result_data = JSON.parse(data);
                if(result_data.is_success){
                    var result_text = result_data.result;
                    document.title = "Result Page";
                    document.getElementById('the_title').innerHTML = "Result";
                    $('#main_page').slideUp(500);
                    $('#result_page').slideDown(1500);                    
                    createAlert('success');               
                }
                else{
                    createAlert('danger');
                }
                document.getElementById('alert_message').innerHTML = result_data.message;
                document.getElementById('alert').style.display = 'block';
                $('#file').slideUp(500);
            },
            error: function(data){
                document.getElementById('alert_message').innerHTML = "An unknown error occurred";
                document.getElementById('alert').style.display = 'block';
                window.location.href = '/';
            }
        });
        e.preventDefault();
    });
});


$(document).ready(function() {
    $('#text').slideUp(0);
    //$('#file').slideUp(0);
    $('#result_page').slideUp(0);
});

$('#text-box').hover(
    function(){$(this).css('box-shadow', '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)');}
    ,function(){$(this).css('box-shadow', '0 0 0 0');
});
$('#file-box').hover(
    function(){$(this).css('box-shadow', '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)');}
    ,function(){$(this).css('box-shadow', '0 0 0 0');
});

$('#text-button').click(function() {
    $('#main_page').slideDown(0);
    $('#text').slideToggle(300);
    $('#file').slideUp(300);
});
    
$('#file-button').click(function() {
    $('#main_page').slideDown(0);
    $('#file').slideToggle(300);
    $('#text').slideUp(300);
});