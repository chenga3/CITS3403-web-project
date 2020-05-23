// This js file is for admin functions in all admin pages
<<<<<<< HEAD

=======
/*** AJAX for REST API ***/
var usertable, user, base_url;
var authToken = null;

window.onload = function() {
    this.setUp();
    base_url = window.location.origin;
}

function setUp() {
    usertable = document.getElementById('usertable-api');
    console.log('setup...');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            responseData = JSON.parse(this.responseText);
            authToken = responseData['token'];
            if (usertable != null) {
                getUsers();
            }
        }
    }
    xhttp.open('POST', '/api/tokens', true);
    xhttp.send();
}

function getUsers() {
    console.log('getting users...');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        //console.log(this.readyState);
        //console.log(this.status);
        if (this.readyState == 4 && this.status == 200) {
            responseData = JSON.parse(this.responseText);
            userList = responseData['userList'];
            renderTable(userList);
        }
    }
    xhttp.open('GET', '/api/users', true);
    xhttp.setRequestHeader("Authorization", "Bearer " + authToken);
    xhttp.send();
}

/* function editUser(id) {
    console.log('Editing user...');
    console.log(id);
    usertable.hidden = true;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            responseData = JSON.parse(this.responseText);
            user = responseData;
            console.log(user);
        }
    }
    xhttp.open('GET', '/api/users/' + id, true);
    xhttp.send();
} */

function deleteUser(id) {
    console.log(id);
    console.log('Deleting user ' + id + '...');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // responseData = JSON.parse(this.responseText);
            // userList = responseData['userList'];
            tr = document.getElementById('user' + id);
            tr.remove();
        }
    }
    xhttp.open('DELETE', '/api/users/' + id, true);
    xhttp.setRequestHeader("Authorization", "Bearer " + authToken);
    xhttp.send();
}

function renderTable(userList) {
    for (var i=0; i<userList.length; i++) {
        console.log(userList[i]);
        tr = document.createElement('tr');
        tr.id = 'user' + userList[i].id;

        td = document.createElement('td');
        td.innerHTML = userList[i].username;
        tr.appendChild(td);

        td = document.createElement('td');
        td.innerHTML = userList[i].email;
        tr.appendChild(td);

        td = document.createElement('td');
        td.innerHTML = (userList[i].admin) ? "Admin" : "User";
        tr.appendChild(td);

        td = document.createElement('td');
        button = document.createElement('button');
        button.innerHTML = 'edit';
        button.classList.add('edit');
        button.value = userList[i].id;
        button.onclick = function(ev) { location.href = base_url + '/admin/' + ev.target.value + '/edituser'; };
        td.appendChild(button);
        tr.appendChild(td);

        td = document.createElement('td');
        button = document.createElement('button');
        button.innerHTML = 'delete';
        button.classList.add('delete');
        button.value = userList[i].id;
        button.onclick = function(ev) { 
                var result = confirm("Are you sure you want to delete");
                if (result) {
                    deleteUser(ev.target.value);
                }
            }
        td.appendChild(button);
        tr.appendChild(td);

        usertable.appendChild(tr);
    }
}

function renderUserForm(user) {
    
}



/*** OTHER FUNCTIONS ***/
>>>>>>> c1d62354... token authentication
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
            alert("some inputs are empty");
            return
        }
        var testcases = []
        var inputs = document.getElementsByClassName("testinput");
        var outputs = document.getElementsByClassName("testoutput");
        for (var i = 0; i < inputs.length ; i++) {
            input = inputs[i].value;
            output = outputs[i].value;
            if (input == "" || output == "") {
                alert("test cases are empty");
                return
            }
            testcases.push({"input": inputs[i].value, 
                            "output": outputs[i].value});
        }
        
        var packet = {
            "title": $("#problemTitle").val(),
            "diff": $("#difficulty").val(),
            "time": $("#timeLimit").val(),
            "question": editor.getValue(),
            "testcases": testcases
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
                alert("error");
           }
       });
});

$(document).on("click", ".tablinks",function(event) {
    id = event.target.value; $(".tabcontent").addClass("tabcontenthidden").removeClass("tabcontent");
    $("#" + id +"").addClass("tabcontent").removeClass("tabcontenthidden");
});

var n = $('.tablinks').length;
$(document).ready(function() {
    $("#addtest").click(function() {
        button = "<button value=\"testCase" + ++n + "\" class=\"tablinks\"" +
        "id=\"tab" + n + "\">Test Case " + n + "</button>";
        $("#addtest").before(button);

        testcasediv = "<div id=\"testCase" + n + "\" class=\"tabcontenthidden\">" +
                        "<textarea placeholder=\"Input\" class=\"testinput\" name=\"input\" id=\"input" + n + "\" cols=\"30\" rows=\"10\"></textarea>" +
                        "<textarea placeholder=\"Output\" class=\"testoutput\"name=\"output\" id=\"output" + n + "\" cols=\"30\" rows=\"10\"></textarea>"+
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

$(document).on("click", "#edit", function() {
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
        
        oldUrlTitle = window.location.pathname.split("/")
        oldUrlTitle = oldUrlTitle[oldUrlTitle.length - 1] 
        var packet = {
            "oldurltitle": oldUrlTitle,
            "title": $("#problemTitle").val(),
            "diff": $("#difficulty").val(),
            "time": $("#timeLimit").val(),
            "question": editor.getValue(),
            "testcases": testCases
        }
       $.ajax({
            url: '/admin/question',
            data: JSON.stringify(packet),
            type: 'PUT',
            contentType: 'application/json',
            success: function(response) {
                alert(response);
            },
            error: function(response) { 
                alert("ERROR");
           }
       });
});

$(document).on("click", ".delete", function() {
        if (confirm("Please confirm u want to delete this question")) {
            urlTitle = $(this).val();
            var packet = {
                "urltitle": urlTitle
            }
            $.ajax({
                url: '/admin/question',
                data: JSON.stringify(packet),
                type: 'DELETE',
                contentType: 'application/json',
                success: function(response) {
                    alert(response);
                },
                error: function(response) { 
                    alert("ERROR");
            }
            });
        } else {
            // do nothings
            return
        }
});


