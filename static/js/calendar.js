let date = new Date();

const renderCalender = () => {
  const viewYear = date.getFullYear();
  const viewMonth = date.getMonth();

  document.querySelector('.year-month').textContent = `${viewYear}년 ${viewMonth + 1}월`;

  const prevLast = new Date(viewYear, viewMonth, 0);
  const thisLast = new Date(viewYear, viewMonth + 1, 0);

  const PLDate = prevLast.getDate();
  const PLDay = prevLast.getDay();

  const TLDate = thisLast.getDate();
  const TLDay = thisLast.getDay();

  const prevDates = [];
  const thisDates = [...Array(TLDate + 1).keys()].slice(1);
  const nextDates = [];

  if (PLDay !== 6) {
    for (let i = 0; i < PLDay + 1; i++) {
      prevDates.unshift(PLDate - i);
    }
  }

  for (let i = 1; i < 7 - TLDay; i++) {
    nextDates.push(i);
  }

  const dates = prevDates.concat(thisDates, nextDates);
  const firstDateIndex = dates.indexOf(1);
  const lastDateIndex = dates.lastIndexOf(TLDate);

  dates.forEach((date, i) => {
    let condition = i >= firstDateIndex && i < lastDateIndex + 1
      ? 'this'
      : 'other';
    
    if (condition === 'other') {
      condition = i < firstDateIndex
        ? condition + ' pre'
        : condition + ' next';
    }

    dates[i] = `<div class="date"><span class="${condition}">${date}</span></div>`;
  });

  document.querySelector('.dates').innerHTML = dates.join('');

  const today = new Date();
  if (viewMonth === today.getMonth() && viewYear === today.getFullYear()) {
    for (let date of document.querySelectorAll('.this')) {
      if (+date.innerText === today.getDate()) {
        date.classList.add('today');
        break;
      }
    }
  }
};

renderCalender();

const prevMonth = () => {
  date.setMonth(date.getMonth() - 1);
  renderCalender();
};

const nextMonth = () => {
  date.setMonth(date.getMonth() + 1);
  renderCalender();
};

const goToday = () => {
  date = new Date();
  renderCalender();
};



// ... (기존 코드)

// day.forEach((items) => {
//   items.addEventListener('click', (e) => {
      // 기존 클릭 이벤트 코드

      // 새로운 부분: 날짜 클릭 시 선택한 날짜를 특정 요소에 표시
      // if (Number(items.innerHTML)) {
      //     const selectedDate = `${selMonth} ${items.innerHTML}`;
      //     document.querySelector('.selected-date').textContent = selectedDate;
      // }

      // 기존 AJAX 요청 코드
  // });
// });

// ... (기존 코드)

// 선택한 날짜를 구체적으로 표시할 엘리먼트를 찾아야 합니다.
// 여기서는 예시로 <p class="selected-date"></p>를 추가하여 사용합니다.
