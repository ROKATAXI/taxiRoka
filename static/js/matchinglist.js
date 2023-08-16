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