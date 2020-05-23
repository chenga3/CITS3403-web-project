var editor = ace.edit("editor");
// editor.setKeyboardHandler("ace/keyboard/vim");
editor.setFontSize("18px");
editor.getSession().setMode("ace/mode/c_cpp");



$(document).ready( function() {
    $( "#language" ).change(function() {
        if ($(this).val() == "cpp") {
            editor.getSession().setMode("ace/mode/c_cpp");
        }
        if ($(this).val() == "py") {
            editor.getSession().setMode("ace/mode/python");
        }
    });
});

$(document).ready(function() {
    $("#submit").click(function() {
        $("#submit").attr("disabled", true);
        var urlTitle = window.location.pathname;
        urlTitle =  urlTitle.split("/");
        urlTitle =  urlTitle[urlTitle.length - 1];
        var packet = {
            "urlTitle": urlTitle,
            "language": $("#language").val(),
            "code": editor.getValue()
        }
       var language = $("#language").val();
       $("#results").empty();
       $("#results").append('<p>Waiting...</p>');
       $.ajax({
            url: '/judge',
            data: JSON.stringify(packet),
            type: 'POST',
            contentType: 'application/json',
            success: function(response) {
                $("#results").empty();

                if (response.hasOwnProperty('error')){
                    $("#results").append('<p>Error</p>');
                    s = response['error'].split("\n");
                    console.log(s);
                    temp = "<pre>" + response["error"] + "</pre>";
                    $("#results").append(temp);
                    
                }
                else {
                    $("#results").append('<p>Result</p>');
                    for (i in response) {
                        console.log(response);
                        if (i == "pass") {
                            continue
                        }
                        if (response[i].includes("Failed")) {
                            s = "<p>Test Case " + (parseInt(i) + 1) + " " + response[i] + "</p>";
                        }
                        else {
                            s = "<p>Test Case " + (parseInt(i) + 1) + ": " + response[i] + "</p>";
                        }
                        $("#results").append(s);
                    }
                    if (response["pass"] == "yes") {
                        $("#results").append('<p>Passed! Well Done :)</p>');
                    }
                    else {
                        $("#results").append('<p>Failed. Please Try Again</p>');
                    }
                }
                $("#submit").attr("disabled", false);
            },
            error: function(response) { 

                $("#results").empty();
                $("#results").append('<p>Failed To Query Judge</p>');
                alert("ERROR");
                $("#submit").attr("disabled", false);
           }
       });
    });
});
