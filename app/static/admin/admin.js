// This js file is for admin functions in all admin pages

//Adding a new user
function addUser() {
    var username = document.getElementById("username").value.trim();
    var email = document.getElementById("email").value.trim();
    var password = document.getElementById("password").value.trim();
    var comfirmp = document.getElementById("confirmp").value.trim();
    // the regulation expression for email and password validation
    var regxemail =/^([a-zA-Z0-9\.-]+)@([a-zA-Z0-9-]+).([a-z]{2,15})(.[a-z]{2,10})?$/;
    var regxpass =/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-\.]).{8,16}$/;

    //input validation
    if(username == "" || email == "" || password == "" || comfirmp == "" ){
        alert("Any inputs should not be empty");
        return false;
    }
    else if (regxemail.test(email)==false){
        alert("The email address is not valid")
        return false;
    }
    else if (regxpass.test(password)==false){
        alert("Password should be at least 8 characters and no more than 16. It also should contain at least one upper case, one lower case, one digit and one special character.");
        return false;
    }
    else if(email != comfirmp){
        alert("The password should be same and not include space element");
        return false;
    }
    
    else {
        return true;
    }
}



//edit the user
function editUser() {
    var username = document.getElementById("username").value.trim();
    var email = document.getElementById("email").value.trim();
    var password = document.getElementById("password").value.trim();
    var regxemail =/^([a-zA-Z0-9\.-]+)@([a-zA-Z0-9-]+).([a-z]{2,15})(.[a-z]{2,10})?$/;
    var regxpass =/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-\.]).{8,16}$/;

    if(username == "" || email == "" || password == ""){
        alert("Any inputs should not be empty");
        return false;
    }
    else if (regxemail.test(email)==false){
        alert("The email address is not valid")
        return false;
    }
    else if (regxpass.test(password)==false){
        alert("Password should be at least 8 characters and no more than 16. It also should contain at least one upper case, one lower case, one digit and one special character.");
        return false;
    }
    else {
        return true;
    }
}


//for post assess
function postAssess() {
    var feedback = document.getElementById("feedback").value.trim();
    if(feedback == ""){
        alert("Feedback should not be empty");
        return false;
    }
    return true;
}

//Adding a new question
function validateQuestion() {
    var title = document.getElementById("problemTitle").value.trim();
    if(title == "" || editor.getValue() == ""){
        return false;
    }
    return true;
}

$(document).on("click", "#submit", function() {
        if(!validateQuestion()) {
            alert("Some inputs are empty");
            return
        }
        var testCases = []
        var inputs = document.getElementsByClassName("testinput");
        var outputs = document.getElementsByClassName("testoutput");
        for (var i = 0; i < inputs.length ; i++) {
            input = inputs[i].value;
            output = outputs[i].value;
            if (input == "" || output == "") {
                alert("Test Cases are empty");
                return
            }
            testCases.push({"input": inputs[i].value, 
                            "output": outputs[i].value});
        }
        
        var packet = {
            "title": $("#problemTitle").val(),
            "diff": $("#difficulty").val(),
            "time": $("#timeLimit").val(),
            "question": editor.getValue(),
            "testcases": testCases
        }
       $.ajax({
            url: '/admin/addquestion',
            data: JSON.stringify(packet),
            type: 'POST',
            contentType: 'application/json',
            success: function(response) {
                alert(response);
            },
            error: function(response) { 
                alert("ERROR");
           }
       });
});

$(document).on("click", ".tablinks",function(event) {
    id = event.target.value;
    $(".tabcontent").addClass("tabcontenthidden").removeClass("tabcontent");
    $("#" + id +"").addClass("tabcontent").removeClass("tabcontenthidden");
});

var n = 1;
$(document).ready(function() {
    $("#addtest").click(function() {
        button = "<button value=\"testCase" + ++n + "\" class=\"tablinks\"" +
        "id=\"tab" + n + "\">Test Case " + n + "</button>";
        $("#addtest").before(button);

        testcasediv = "<div id=\"testCase" + n + "\" class=\"tabcontenthidden\">" +
                        "<textarea class=\"testinput\" name=\"input\" id=\"input" + n + "\" cols=\"30\" rows=\"10\"></textarea>" +
                        "<textarea class=\"testoutput\"name=\"output\" id=\"output" + n + "\" cols=\"30\" rows=\"10\"></textarea>"+
                        "</div>";

        $("#testCase" + (n - 1) + "").after(testcasediv);

        $(".tabcontent").addClass("tabcontenthidden").removeClass("tabcontent");
        $("#testCase" + n +"").addClass("tabcontent").removeClass("tabcontenthidden");

    });
});

$(document).on("click", "#removetest",function() {
    if (n == 1) {
        return;
    }
    n--;
    var number = $(".tabcontent").attr("id");
    number = number.charAt(number.length -1);
    $("#tab" + number +"").remove();
    $("#testCase" + number +"").remove();
    var buttons = document.getElementsByClassName("tablinks");
    for(var i = 0; i < buttons.length ; i++) {
        buttons[i].setAttribute("id", "tab"+(i+1));
        buttons[i].setAttribute("value", "testCase"+(i+1));
        buttons[i].innerHTML = "Test Case "+(i+1);
    }

    var content = document.getElementsByClassName("tabcontenthidden");
    for(var i = 0; i < content.length; i++) {
        var textarea = content[i].children;
        textarea[0].setAttribute("id", "input"+(i+1));
        textarea[1].setAttribute("id", "output"+(i+1));
        content[i].setAttribute("id", "testCase"+(i+1));
    }
    $("#testCase1").addClass("tabcontent").removeClass("tabcontenthidden");
});
