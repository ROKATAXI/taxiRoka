// 버튼 클릭 시 모달 창 띄우기
const signupButton = document.getElementById('signupBtn');
const modal = document.getElementById('myModal');
const closeBtn = document.getElementsByClassName('close')[0];

signupButton.addEventListener('click', function() {
    modal.style.display = 'block';
});

closeBtn.addEventListener('click', function() {
    modal.style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
