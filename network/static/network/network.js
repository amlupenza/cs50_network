window.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll('.follow-btn').forEach((btn)=>{
        let user_id = btn.dataset.id;
        btn.onclick = ()=> follow_user(user_id);
    });
    // show sidebar
    document.querySelector('#showMenu').onclick = ()=>{
        document.querySelector("#navbar-left").style.display = 'block';
        document.querySelector('#topDiv').style.display = 'none';
    };
    // hide sidebar 
    document.querySelector('#hideMenu').onclick = () => {
        document.querySelector("#navbar-left").style.display = 'none';
        document.querySelector('#topDiv').style.display = 'block';
    }
    document.querySelector('#followingBtn').onclick = ()=>{
        // hide allposts div
        console.log('following is clicked')
        document.querySelector('#allposts').style.display = 'none';
        // show followingposts div
        document.querySelector('#followingPosts').style.display = 'block';
    };
    document.querySelectorAll('.fa-pen-to-square').forEach((btn) => {
        let postId = btn.dataset.edit;
        btn.onclick = () => {
            console.log(`edit of id ${postId} has been clicked`)
            editPost(postId);
        }
    });
    document.querySelectorAll('.likeIcon').forEach((btn)=>{

        btn.onclick = () =>{
            [post_type, post_id] = btn.dataset.like.split('-');
            console.log(`post id is ${post_id} is clicked`)
            like_post(post_type,post_id);
        }
    });
   
})
// select like button when page has already loaded
document.querySelector('body').addEventListener('click',event=>{
    if(event.target.matches('.likeIcon')){
        let btn = event.target;
        let [post_type,post_id] = btn.dataset.like.split('-');
        // call like function
        like_post(post_type,post_id);
    }
    
});


// follow_user function
function follow_user(userId){
    console.log(userId)
    // get follow button by its id
    let follow_btn = document.getElementById(`follow-btn-${userId}`);
    let followingsElement = document.getElementById(`followings-${userId}`);
    let followersElement = document.getElementById(`followers-${userId}`)
    console.log(follow_btn)
    fetch(`/follow/${userId}`,{
        method : 'POST',
    })
    .then(response =>response.json())
    .then(data => {
        // update followers
        console.log(data.followers)
        followersElement.innerHTML = data.followers
        followingsElement.innerHTML = data.followings
        // check if is following the account
        if (data.followed){
            
            follow_btn.textContent = 'Unfollow';
          
        }else{
            follow_btn.textContent = 'Follow';

        }
    })
    .catch(error => {
        console.error(error);
    });
}

// edit post function

function editPost(postId){
    fetch(`/editPost/${postId}`)
    .then(response => response.json())
    .then(data =>{
        let div = document.createElement('div');
        div.className = 'editCont';
        div.innerHTML =`<form action='#' method='post' id='editform'><h5>${data.author}, do you want to edit this post?</h5><textarea name="newPost" id="newPost" cols="30" rows="10">${data.tweet}</textarea><div class='row gw-2'><input type='submit' value='Save changes' class='col-md btn btn-primary'><button class='col-md btn btn-danger' id='cancel-edit'>Cancel</button></div></form>`;
        document.body.appendChild(div);
        document.querySelector('#cancel-edit').onclick = () => div.remove();
        let form = document.querySelector('#editform');
        form.onsubmit = (event)=>{
            event.preventDefault();
            // tweet paragraph element
            console.log(postId)
            let tweetpar = document.querySelector(`#tweet-${postId}`)
            let newPost = document.querySelector('#newPost').value
            fetch(`/editPost/${postId}`, {
                method : 'POST',
                headers : {
                    'content-type': 'application/json',
                },
                body : JSON.stringify({newPost: newPost})
            })
            .then(response =>{
                tweetpar.innerHTML = newPost;
                div.remove();
            })
            .catch(error =>{
                console.error('error:',error);
            });
        }
    })
}

// like post function
function like_post(post_type, postId){
    console.log(`postid is ${postId}`)
    console.log(`post type is ${post_type}`)
    fetch(`/likePost/${post_type}/${postId}`, {
        method : 'POST'
    })
    .then(response => response.json())
    .then(data => {
        likes = data.likes;
        console.log(`this has ${likes} likes`)
        post_type = data.post_type;
        document.querySelector(`#post-likes-${postId}`).innerHTML = likes;
        console.log(`like? ${data.liked}`)
        if(data.liked){
            document.querySelector(`#${post_type}-like-${postId}`).style.color = 'red';
        }
       else{
            document.querySelector(`#${post_type}-like-${postId}`).style.color = 'black';
        }
        
    })
}