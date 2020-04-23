// This file is for checking whether there are any empty entry or different password

// for register page checking both empty and different password
var btn = document.getElementById("sub");
btn.addEventListener("click",isempty);
btn.addEventListener("click",isequal);

// check the input is empty or not
function isempty() {
    if (document.getElementById("user").value.length==0 || document.getElementById("email").value.length==0 || document.getElementById("p1").value.length==0 || document.getElementById("p2").value.length==0){
        alert("Any of inputs should not be empty!");
        return false;
    }
    return true;
}

// check the password is empty or not
function isequal(){
    if(document.getElementById("p1").value != document.getElementById("p2").value){
        alert("The password should be same");
        return false;
    }
    return true;
}
