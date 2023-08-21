followBtn=document.getElementById("follow")
console.log(followBtn.innerHTML)
if (followBtn.innerHTML=="unfollow"){
    followBtn.className="btn btn-danger"


}
if (followBtn.innerHTML=="follow"){
    followBtn.className="btn btn-success"
    

}

