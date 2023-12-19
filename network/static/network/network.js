window.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll('.follow-btn').forEach((btn)=>{
        let user_id = btn.dataset.id;
        btn.onclick = ()=> follow_user(user_id);
    });
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
    })
})

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
        div.innerHTML =`<form action='#' method='post' id='editform'><h5>${data.author}</h5><textarea name="newPost" id="newPost" cols="30" rows="10">${data.tweet}</textarea><input type='submit' value='Save changes' class='btn-primary'><button class='btn-danger' id='cancel-edit'>Cancel</button></form>`;
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