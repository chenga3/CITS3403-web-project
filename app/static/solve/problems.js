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