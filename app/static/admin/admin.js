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