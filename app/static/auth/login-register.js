// This file is for checking whether there are any empty entry or different password

// check the input is empty or not
function isempty() {
    if (document.getElementById("user").value.trim() == "" || document.getElementById("p0").value.trim() == ""){
        alert("Any of inputs should not be empty");
        return false;
    }
    return true;
}

// for register page checking input empty and same password
function validate(){
    // regular expression for validation
    var regxemail =/^([a-zA-Z0-9\.-]+)@([a-zA-Z0-9-]+).([a-z]{2,15})(.[a-z]{2,10})?$/;
    var regxpass =/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-\.]).{8,16}$/;
    if (document.getElementById("user").value.trim() == "" || document.getElementById("email").value.trim() == "" || document.getElementById("p1").value.trim() == "" || document.getElementById("p2").value.trim() == ""){
        alert("Any of inputs should not be empty");
        return false;
    }
    else if (regxemail.test(document.getElementById("email").value.trim())==false){
        alert("The email address is not valid")
        return false;
    }
    else if (regxpass.test(document.getElementById("p1").value.trim())==false){
        alert("Password should be at least 8 characters and no more than 16. It also should contain at least one upper case, one lower case, one digit and one special character.");
        return false;
    }
    else if(document.getElementById("p1").value.trim() != document.getElementById("p2").value.trim()){
        alert("The password should be same and do not use space element");
        return false;
    }
    else{
        return true;
    }
}