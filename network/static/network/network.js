window.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll('.follow-btn').forEach((btn)=>{
        let user_id = btn.dataset.id
        btn.onclick = ()=> follow_user(user_id);
    });
    document.querySelector('#followingBtn').onclick = ()=>{
        // hide allposts div
        console.log('following is clicked')
        document.querySelector('#allposts').style.display = 'none';
        // show followingposts div
        document.querySelector('#followingPosts').style.display = 'block';
    };
    document.querySelector('#forYoubtn').onclick = () =>{
        console.log('forYou btn is clicked')
        // show allposts div
        document.querySelector('#allposts').style.display = 'block';
        // hide followingposts div
        document.querySelector('#followingPosts').style.display = 'none';
    };
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