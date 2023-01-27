// to change the color of username text when the input is active.
let user = document.getElementById("labelUsername");
let password = document.getElementById("labelPassword");
var user_input = document.getElementById("inputUsername");
var user_pass = document.getElementById("inputPassword");

user_input.addEventListener('click',highlightuser);
user_pass.addEventListener('click',highlightpass);


function highlightuser(){
    user.style.color = "#eddabf";
    password.style.color = "white";
    password.style.transform = "translate(2px,-75px)"
    }

function highlightpass(){
    password.style.color = "#eddabf";
    user.style.color = "white";
    user.style.transform = "translate(2px,75px)"

    }


