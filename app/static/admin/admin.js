// This js file is for admin functions in all admin pages
/*** AJAX for REST API ***/
var usertable, user;

window.onload = function() {
    this.setUp();
}

function setUp() {
    usertable = document.getElementById('usertable-api');
    console.log('setup...');
    getUsers();
}


function getUsers() {
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
    xhttp.send();
}

function editUser(id) {
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
}

function renderTable(userList) {
    for (i=0; i<userList.length; i++) {
        console.log(userList[i]);
        tr = document.createElement('tr');

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
        button.onclick = function(ev) { editUser(ev.target.value); };
        td.appendChild(button);
        tr.appendChild(td);

        td = document.createElement('td');
        button = document.createElement('button');
        button.innerHTML = 'delete';
        button.classList.add('delete');
        td.appendChild(button);
        tr.appendChild(td);

        usertable.appendChild(tr);
    }
}

function renderUserForm(user) {
    
}



/*** OTHER FUNCTIONS ***/
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

//Adding a new question
function validateQuestion() {
    var title = document.getElementById("titlename").value.trim();
    if(title == ""){
        alert("Any inputs should not be empty");
        return false;
    }
    return true;
}

//edit the user
/* function editUser() {
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
} */


//import internet editor in the content
ClassicEditor.create( document.querySelector( '#content' ), {
        toolbar: [ 'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote' ],
        heading: {
            options: [
                { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
                { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
                { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' }
            ]
        }
    } )
    .catch( error => {
        console.log( error );
    } );

//for post assess
function postAssess() {
    var feedback = document.getElementById("feedback").value.trim();
    if(feedback == ""){
        alert("Feedback should not be empty");
        return false;
    }
    return true;
}

