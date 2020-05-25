var editor = ace.edit("editor");
// editor.setKeyboardHandler("ace/keyboard/vim");
editor.setFontSize("18px");
editor.getSession().setMode("ace/mode/c_cpp");
var authToken = null;

jQuery(function() {
    setUp();

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
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + authToken);
            },
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

function setUp() {
    $.ajax({
        url: '/api/tokens',
        type: 'post',
        success: function(result) {
            authToken = result['token'];
            // console.log(authToken);
        }
    })

    $( "#language" ).change(function() {
        if ($(this).val() == "cpp") {
            editor.getSession().setMode("ace/mode/c_cpp");
        }
        if ($(this).val() == "py") {
            editor.getSession().setMode("ace/mode/python");
        }
    });
}

function showFirstSlide() {
    //change the slides background picture
    const slideshow = document.querySelector("#slideshow");
    slideshow.style.backgroundImage = "url('/static/images/codeimage.jpg')";
    slideshow.classList.add("slideshowstyle");

    //change the slides classes
    const box = document.querySelector("slideshowbox");
    slideshowbox.classList.remove("slideshowbox2");
    slideshowbox.classList.add("slideshowbox1");

    //change the slides header text
    const header = document.querySelector("#slideshowheader");
    header.textContent = "Large question bank";

    //change the slides body text
    const son = document.querySelector("#slideshowdescription");
    son.textContent = "Learn from a sizeable question bank with variety and varying levels of difficulty to choose from";

    //set timer to call the other slide
    setTimeout(() => showSecondSlide(), 5000);
}

//show the first slide
function showSecondSlide() {
    //change the slides background picture
    const slideshow = document.querySelector("#slideshow");
    slideshow.style.backgroundImage = "url('/static/images/interviewimage.jpg')";

    //change the slides classes
    const box = document.querySelector("slideshowbox");
    slideshowbox.classList.remove("slideshowbox1")
    slideshowbox.classList.add("slideshowbox2");

    //change the slides header text
    const header = document.querySelector("#slideshowheader");
    header.textContent = "Effective Interview Training";

    //change the slides body text
    const son = document.querySelector("#slideshowdescription");
    son.textContent = "Polish your interview question cracking skills by tackling our stimulating questions";

    //set timer to call the other slide
    setTimeout(() => showFirstSlide(), 5000);
}