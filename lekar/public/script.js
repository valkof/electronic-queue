const appointment = document.querySelector('.appointment');
const offices = document.querySelector('.offices');
const rooms = document.querySelectorAll('.room');
const sections = document.querySelectorAll('.office');
const monthsSets = document.querySelectorAll('.months');
const months = document.querySelectorAll('.month__button');
const breadcrumb = document.querySelector('.breadcrumb');
const persona = document.querySelector('.persona');
const breadcrumbButtonOffice = document.getElementById('breadcrumb-button-office');
const breadcrumbButtonRoom = document.getElementById('breadcrumb-button-room');
const breadcrumbButtonMonth = document.getElementById('breadcrumb-button-month');
const breadcrumbButtonDay = document.getElementById('breadcrumb-button-day');
const breadcrumbButtonTime = document.getElementById('breadcrumb-button-time');
const breadcrumbButtonPrint = document.getElementById('breadcrumb-button-print');


sections.forEach(section => {
  const button = section.querySelector('.office__button');  
  // const buttons = section.querySelector('.buttons');  
  button.addEventListener('click', () => {
    // Скрываем все кнопки и показываем активную
    sections.forEach(office => {
      office.classList.remove('office-active');
    });
    section.classList.add('office-active');
    
    appointment.classList.remove('appointment-active');
    // buttons.classList.add('display_none');
    // breadcrumb.classList.add('display_block');
    // persona.classList.add('display_block');
    // offices.classList.add('display_block');

    breadcrumbButtonOffice.innerHTML = button.innerHTML;
    breadcrumbButtonOffice.onclick = button.onclick;
  });
});

rooms.forEach(room => {
  const button = room.querySelector('.room__button');
  const span = button.querySelector('span');

  button.addEventListener('click', () => {
    rooms.forEach(elem => {
      elem.classList.remove('room-active');
    })
    room.classList.add('room-active');

    breadcrumbButtonRoom.innerHTML = span.innerHTML;
    breadcrumbButtonRoom.onclick = button.onclick;
  })

})

monthsSets.forEach(monthsSet => {
  const monthsByRoom = monthsSet.querySelectorAll('.month__button');
  monthsByRoom.forEach(month => {
    month.addEventListener('click', () => {
      months.forEach(elem => {
        elem.classList.remove('month-active');
      });
      monthsSets.forEach(elem => {
        elem.classList.remove('month-active');
      });
      month.classList.add('month-active');
      monthsSet.classList.add('months-active');
  
      breadcrumbButtonMonth.innerHTML = month.value;
      breadcrumbButtonMonth.onclick = month.onclick;
    })

  })
})

function dayActive(event) {
  console.log(event);
  const daysWrapper = document.querySelector('.days__wrapper');
  const days = daysWrapper.querySelectorAll('.day');
  days.forEach(day => {
    day.classList.remove('day-active');
  });

  event.parentElement.classList.add('day-active');
  daysWrapper.classList.add('days__wrapper-active');

  const dayNumber = event.querySelector('.number').innerHTML;
  const dayWeek = event.querySelector('.week').innerHTML;
  breadcrumbButtonDay.innerHTML = dayNumber + ' ' + dayWeek;
  breadcrumbButtonDay.onclick = event.onclick;
}


function couponGenerated(value, nVid_, nGr_l, nNum_, sTarget_, sAddn_, sAction_) {
  breadcrumbButtonTime.innerHTML = value;
  breadcrumbButtonPrint.onclick = () => {
    jsa_031(nVid_, nGr_l, nNum_, sTarget_, sAddn_, sAction_);
  }
}