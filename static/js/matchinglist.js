
const slider = document.querySelector('.slider');
const slides = document.querySelectorAll('.slide');
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
let currentIndex = 0;

function showSlide(index) {
  const slideWidth = slides[0].offsetWidth;
  slider.style.transform = `translateX(-${index * slideWidth}px)`;

  // 첫 번째 슬라이드에서는 왼쪽 버튼 비활성화
  if (index === 0) {
    prevButton.disabled = true;
  } else {
    prevButton.disabled = false;
  }

  // 세 번째 슬라이드에서는 오른쪽 버튼 비활성화
  if (index === slides.length - 1) {
    nextButton.disabled = true;
  } else {
    nextButton.disabled = false;
  }
}

function prevSlide() {
  // 첫 번째 슬라이드에서는 이전 슬라이드로 이동하지 않음
  if (currentIndex === 0) {
    return;
  }

  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  showSlide(currentIndex);
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
}

// Show the initial slide
showSlide(currentIndex);

// Button click event listeners
prevButton.addEventListener('click', prevSlide);
nextButton.addEventListener('click', nextSlide);



// 오늘 날짜 객체 생성
const today = new Date();

// 날짜 정보 추출
const year = today.getFullYear();
const month = today.getMonth() + 1;
const day = today.getDate();

// 태그에 오늘 일수 넣기
const todaysDateTag = document.getElementById('todaysDate');
todaysDateTag.textContent = `${day}`;


const daysOfWeek = ['일', '월', '화', '수', '목', '금', '토'];
const date = new Date(year, month - 1, day);
const dayOfWeek = date.getDay();
  
  

// // 태그에 오늘 요일 넣기
const todaysDay = daysOfWeek[dayOfWeek];
const todaysDayTag = document.getElementById('todaysDay');
todaysDayTag.textContent = `${todaysDay}`;






// n일 뒤의 날짜 계산
const dayn = 0; // 예를 들어, 7일 뒤의 날짜를 구하려면 n 값을 7로 설정
const nDaysLater = new Date(today);
// nDaysLater.setDate(today.getDate() + dayn);

// 결과 출력
console.log(`${year}-${month}-${day}`);
