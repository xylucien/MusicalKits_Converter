'use strict';
    
// feature detection for drag&drop upload
var isAdvancedUpload = function()
    {
        var div = document.createElement( 'div' );
        return ( ( 'draggable' in div ) || ( 'ondragstart' in div && 'ondrop' in div ) ) && 'FormData' in window && 'FileReader' in window;
    }();

// applying the effect for every form
var forms = document.querySelectorAll( '.box' );
var text_form = document.getElementById('text_input');

function logSubmit(e) {
    var form_data = new FormData();
        form_data.append('text', document.getElementById("textcontent").value);
        $.ajax({
            type: 'POST',
            url: '/convert_result/submission',
            data: form_data,
            contentType: false,
            processData: false,
            success: function(data) {
                var result_text = JSON.parse(data).result;
                document.title = "Result Page";
                document.getElementById('the_title').innerHTML = "Result";
                document.getElementById('result_content').innerHTML = result_text;
                if(result_text==="There is something wrong with your input. Please check again!"){
                    document.getElementById('download').style.display = "none";
                }                        
                $('#main_page').slideUp(500);
                $('#result_page').slideDown(1500);
            },
            error: function(data){
                window.location.href = '/';
            }
        });
        e.preventDefault();
}
text_form.addEventListener('submit', logSubmit);
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
                form.classList.remove( 'is-uploading' );
                document.title = "Result Page";
                $('#main_page').slideUp(500);
                $('#result_page').slideDown(1500);
                document.getElementById('the_title').innerHTML = "Result";
                document.getElementById('result_content').innerHTML = JSON.parse(data).result;
            },
            error: function(data){
                window.location.href = '/';
            }
        });
        e.preventDefault();
    });
});


$(document).ready(function() {
    $('#text').slideUp(0);
    $('#file').slideUp(0);
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
    $('#text').slideToggle(300);
    $('#file').slideUp(300);
    });
    
    $('#file-button').click(function() {
    $('#file').slideToggle(300);
    $('#text').slideUp(300);
    });