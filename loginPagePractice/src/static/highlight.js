// to change the color of username text when the input is active.
let user = document.getElementById("labelUsername");
let password = document.getElementById("labelPassword");
var user_input = document.getElementById("inputUsername");
var user_pass = document.getElementById("inputPassword");

user_input.addEventListener('focus',highlightuser);
user_input.addEventListener('blur',blurUser);
user_pass.addEventListener('focus',highlightpass);
user_pass.addEventListener('blur',blurPass);


function blurUser() {
    user.style.color = "#eddabf";
}
function blurPass() {
    password.style.color = "#eddabf";
}

function highlightuser(){
    password.style.color = "#eddabf";
    user.style.color = "white";
    }

function highlightpass(){
    user.style.color = "#eddabf";
    password.style.color = "white";
    }


