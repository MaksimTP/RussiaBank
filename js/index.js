window.onscroll = function() {stickyMessageBar()};

var sendMessage = document.getElementById("sendMessage");
var message = document.getElementById("message");
var sticky = message.offsetTop;

function stickyMessageBar() {
    if (window.scrollY >= sticky) {
        message.classList.add("sticky");
        sendMessage.classList.add("sticky");
      } else {
        message.classList.remove("sticky");
        sendMessage.classList.remove("sticky");
      }
    }

function sendMessage() {

}