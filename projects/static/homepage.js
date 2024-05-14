function hideIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:none;");
    navigation.classList.remove("hide");
  }
  
  function showIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:block;");
    navigation.classList.add("hide");
  }
  
  //Comment
  function showComment(){
    var commentArea = document.getElementById("comment-area");
    commentArea.classList.remove("hide");
  }
  
  //Reply
  function showReply(){
    var replyArea = document.getElementById("reply-area");
    replyArea.classList.remove("hide");
  }
// navbar
function toggleNavbar() {
  const navbarBurger = document.querySelector('.navbar-burger');
  const navbarMenu = document.getElementById(navbarBurger.dataset.target);
  navbarBurger.classList.toggle('is-active');
  navbarMenu.classList.toggle('is-active');
}