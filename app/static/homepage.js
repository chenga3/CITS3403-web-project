function showFirstSlide() {
    //change the slides background picture
    const slideshow = document.querySelector("#slideshow");
    slideshow.style.backgroundImage = "url('./images/codeimage.jpg')";
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
    slideshow.style.backgroundImage = "url('./images/interviewimage.jpg')";

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

showFirstSlide();
