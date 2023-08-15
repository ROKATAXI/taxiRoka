var modal = document.getElementById("myModal");
var closeBtn = document.getElementsByClassName("close")[0];

function openModal() {
    modal.style.display = "block";
}

function closeModal() {
    modal.style.display = "none";
}

// 모달 닫기 버튼 클릭 시 모달 닫기
closeBtn.onclick = closeModal;

// 모달 외부 클릭 시 모달 닫기
window.onclick = function (event) {
    if (event.target === modal) {
        closeModal();
    }
}
