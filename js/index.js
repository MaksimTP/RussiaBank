window.onscroll = function() {stickyMessageBar()};

var message = document.getElementById("message");
var sticky = message.offsetTop;

function stickyMessageBar() {
    if (window.scrollY >= sticky) {
        message.classList.add("sticky");
      } else {
        message.classList.remove("sticky");
      }
    }