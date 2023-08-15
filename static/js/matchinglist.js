let date = new Date();

const renderCalender = () => {
  const viewYear = date.getFullYear();
  const viewMonth = date.getMonth();
  const viewDate = date.getDate(); // 오늘 날짜

  document.querySelector('.year-month').textContent = `${viewYear}년 ${viewMonth + 1}월`;

  const today = new Date();
  const startOfWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - today.getDay()); // 이번 주의 시작 날짜

  const dates = [];

  for (let i = 0; i < 7; i++) {
    const currentDate = new Date(startOfWeek.getFullYear(), startOfWeek.getMonth(), startOfWeek.getDate() + i);
    const condition = currentDate.getMonth() === viewMonth ? 'this' : 'other';
    const day = currentDate.getDate();

    dates.push(`<div class="date"><span class=${condition}>${day}</span></div>`);
  }

  document.querySelector('.dates').innerHTML = dates.join('');
};

renderCalender();