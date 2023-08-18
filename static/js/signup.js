document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.querySelector(".logout-container form");
    const passwordInput = document.querySelector('input[name="password"]');
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');
    const modalEmptyFields = document.getElementById("modalEmptyFields");
    const modalMismatchPassword = document.getElementById("modalMismatchPassword");
    const closeModalButtons = document.querySelectorAll(".close");
    const modalShortPassword = document.getElementById("modalShortPassword");
    signupForm.addEventListener("submit", function (event) {
      event.preventDefault();
  
      // 입력하지 않은 필드가 있는지 체크
      const formInputs = signupForm.querySelectorAll("input");
      let emptyFieldFound = false;
      for (const input of formInputs) {
        if (!input.value) {
          emptyFieldFound = true;
          break;
        }
      }
  
      if (emptyFieldFound) {
        modalEmptyFields.style.display = "block";
        return;
      }
  
      // 비밀번호 불일치 시 모달 띄우기
      if (passwordInput.value !== confirmPasswordInput.value) {
        modalMismatchPassword.style.display = "block";
        return;
      }

      if (passwordInput.value.length < 8) {
        modalShortPassword.style.display = "block";
        return;
    }
      // 유효성 검사 통과 시 폼 제출
      signupForm.submit();
    });
  
    // 모달 닫기 버튼 클릭 시 모달 닫기
    closeModalButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        modalEmptyFields.style.display = "none";
        modalMismatchPassword.style.display = "none";
        modalShortPassword.style.display = "none";
      });
    });

  const signupBtn = document.getElementById("signupBtn");

  signupForm.addEventListener("submit", function () {
    signupBtn.disabled = true; // 버튼을 비활성화
  });
  });
  