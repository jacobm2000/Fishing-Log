followBtn=document.getElementById("follow")
var elements = document.getElementsByClassName("like_btn");

var myFunction = function() {
    alert(this.id)
};

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', myFunction, false);
}

if (followBtn.innerHTML=="unfollow"){
    followBtn.className="btn btn-danger"


}
if (followBtn.innerHTML=="follow"){
    followBtn.className="btn btn-success"
    

}

