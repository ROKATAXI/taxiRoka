// 비밀번호 재입력 일치 확인
const passwordInput = document.getElementById('inputPassword3');
const confirmPasswordInput = document.getElementById('confirmPassword');
const signupButton = document.getElementById('signupButton');

confirmPasswordInput.addEventListener('input', () => {
    if (passwordInput.value !== confirmPasswordInput.value) {
        confirmPasswordInput.setCustomValidity('비밀번호가 일치하지 않습니다.');
    } else {
        confirmPasswordInput.setCustomValidity('');
    }
});

// 폼 제출 시 데이터 확인
const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
    event.preventDefault();
    // 여기에 폼 데이터 유효성 검사 및 제출 로직을 작성

    const formInputs = form.querySelectorAll('.form-control');
    let isValid = true;
    formInputs.forEach(input => {
        if (!input.value) {
            isValid = false;
        }
    });

    if (isValid) {
        form.submit();
    } else {
        alert('모든 필드를 입력하세요.');
    }
});