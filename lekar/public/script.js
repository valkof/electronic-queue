const appointment = document.querySelector('.appointment');
const offices = document.querySelector('.offices');
const rooms = document.querySelectorAll('.room');
const sections = document.querySelectorAll('.office');
const months = document.querySelectorAll('.month__button');
const breadcrumb = document.querySelector('.breadcrumb');
const persona = document.querySelector('.persona');
const breadcrumbButtonOffice = document.getElementById('breadcrumb-button-office');
const breadcrumbButtonRoom = document.getElementById('breadcrumb-button-room');
const breadcrumbButtonMonth = document.getElementById('breadcrumb-button-month');
const breadcrumbButtonDay = document.getElementById('breadcrumb-button-day');
const breadcrumbButtonTime = document.getElementById('breadcrumb-button-time');


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

months.forEach(month => {
  month.addEventListener('click', () => {
    months.forEach(elem => {
      elem.classList.remove('month-active');
    })
    month.classList.add('month-active');

    breadcrumbButtonMonth.innerHTML = month.value;
    breadcrumbButtonMonth.onclick = month.onclick;
  })
})