// This js file is for admin functions in all admin pages
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

