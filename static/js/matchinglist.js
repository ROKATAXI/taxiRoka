
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


const daysOfWeek = ['일', '월', '화', '수', '목', '금', '토'];

// 오늘 날짜 객체 생성
const today = new Date();

// 날짜 정보 추출
const year = today.getFullYear();
const month = today.getMonth() + 1;
const day = today.getDate();

// 함수를 통해 slide에 날짜와 요일 추가하는 기능 생성
function addDatesToSlide(slideId, startDay) {
    const slide = document.getElementById(slideId);
    
    for (let dayn = startDay; dayn < startDay + 7; dayn++) {
        const nDaysLater = new Date(today);
        nDaysLater.setDate(today.getDate() + dayn);

        const nyear = nDaysLater.getFullYear();
        const nmonth = nDaysLater.getMonth() + 1;
        const nday = nDaysLater.getDate();

        const ndate = new Date(nyear, nmonth - 1, nday);
        const ndayOfWeek = ndate.getDay();
        const ndaysDay = daysOfWeek[ndayOfWeek];

        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <p id="todaysDate-${dayn}">${nday}</p>
            <p id="todaysDay-${dayn}">${ndaysDay}</p>
        `;

        // 클릭 이벤트 리스너 추가
        listItem.addEventListener('click', () => {
            const clickedDate = `${nyear}-${nmonth.toString().padStart(2, '0')}-${nday.toString().padStart(2, '0')}`;
            const url = `?selected_date=${clickedDate}`;
            window.location.href = url;
        });

        slide.appendChild(listItem);
    }
}

// slide1에 7일치 날짜와 요일 추가
addDatesToSlide('slide1', 0);

// slide2에 다음 7일치 날짜와 요일 추가
addDatesToSlide('slide2', 7);

// slide3에 그 다음 7일치 날짜와 요일 추가
addDatesToSlide('slide3', 14);