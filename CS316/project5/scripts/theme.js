function darkTheme() {
    var bckgrndClr = document.querySelector("html");
    bckgrndClr.style.backgroundColor = "rgb(0,0,0)";
    var hdrClr = document.querySelector("h1");
    hdrClr.style.color = "rgb(0,0,0)";
    var headshot = document.querySelector("#headshot");
    headshot.src = "../images/headshotDark.PNG";
    var navmenu = document.querySelectorAll("nav > a, nav > a:visited");
    for (var i = 0; i < navmenu.length; i++) {
        navmenu[i].style.color = "rgb(0,34,204)";
        navmenu[i].style.backgroundColor = "rgb(102,179,255)";
    }
    var contact = document.querySelector(".contact");
    contact.style.backgroundColor = "rgb(102,179,255)";
    contact.style.border = "5px solid rgb(0,34,204)";
    var contactText = document.querySelectorAll(".contact > p");
    for (var i = 0; i < contactText.length; i++) {
        contactText[i].style.color = "rgb(0,0,0)";
    }
    var contactLinks = document.querySelectorAll("p > a");
    for (var i = 0; i < contactLinks.length; i++) {
        contactLinks[i].style.color = "rgb(0,34,204)";
    }
}

function lightTheme() {
    var bckgrndClr = document.querySelector("html");
    bckgrndClr.style.backgroundColor = "rgb(85,85,85)";
    var hdrClr = document.querySelector("h1");
    hdrClr.style.color = "rgb(255,238,230)";
    var headshot = document.querySelector("#headshot");
    headshot.src = "../images/headshot.PNG";
    var navmenu = document.querySelectorAll("nav > a, nav > a:visited");
    for (var i = 0; i < navmenu.length; i++) {
        navmenu[i].style.color = "rgb(102,179,255)";
        navmenu[i].style.backgroundColor = "rgb(0,34,204)";
    }
    var contact = document.querySelector(".contact");
    contact.style.backgroundColor = "rgb(0,34,204)";
    contact.style.border = "5px solid rgb(102,179,255)";
    var contactLinks = document.querySelectorAll("p > a");
    for (var i = 0; i < contactLinks.length; i++) {
        contacttLinks[i].style.color = "rgb(102,179,255)";
    }
}
var theme = document.getElementById("themeBttn");
theme.addEventListener("click", function(e) {
  if (this.innerHTML == "Light Mode") {
      this.innerHTML = "Dark Mode";
      darkTheme();
  }
  else {
      this.innerHTML = "Light Mode";
      lightTheme();
  }
  e.preventDefault(); // stops page refresh
  // Since the page has been "reloaded", re-show the menu animation
  $("nav, .content, .contact").hide();
  $("nav, .content, .contact").slideDown(750);
});
var navMenuHover = document.querySelectorAll("nav > a");
for (var i = 0; i < navMenuHover.length; i++) {
    navMenuHover[i].addEventListener("mouseover", function() {
        if (theme.innerHTML == "Light Mode") {
            this.style.color = "rgb(255,238,230)";
            this.style.backgroundColor = "rgb(102,179,255)";         }
        else {
            this.style.color = "rgb(0,34,204)";
            this.style.backgroundColor = "rgb(255,238,230)";         }
        });
    navMenuHover[i].addEventListener("mouseout", function() {
        if (theme.innerHTML == "Light Mode") {
            this.style.color = "rgb(102,179,255)";
            this.style.backgroundColor = "rgb(0,34,204)";
        }
        else {
            this.style.color = "rgb(0,34,204)";
            this.style.backgroundColor = "rgb(102,179,255)";
        }
        });
}
// Initial hide and slide down of menu animation
$("nav, .content, .contact").hide();
$("nav, .content, .contact").slideDown(750);
