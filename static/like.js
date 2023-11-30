function like(id){
    const likeCount=document.getElementById('like-count-'+id);
    const likeBtn=document.getElementById('like-btn-'+id);

    fetch('/like/'+id,{method:"POST"})
    .then((res) => res.json())
    .then((data) => {
    likeCount.innerHTML=data["likes"]
    if(data["liked"] ===true){
        likeBtn.className="fas fa-thumbs-up"
    }
    else
    {
        likeBtn.className="far fa-thumbs-up"
    }
    
    }
    )
}