const initial = document.querySelector("#link1");
initial.classList.add("selectedLink");

var links = document.querySelectorAll(".link");
links.forEach(link => link.addEventListener("click", (e) => selectButton(e)));

//changes the colors of the selected button while reverting the colors of the other buttons
function selectButton(e) {
    var id;
    if(e.srcElement.id == ""){
        id = e.srcElement.parentElement.id; 
    }
    else{
        id = e.srcElement.id;
    }
    links.forEach(link => {
        link.classList.remove("selectedLink");
    });
    const currLink = document.querySelector("#" + id);
    currLink.classList.add("selectedLink");
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

// showFirstSlide();