const appointment = document.querySelector('.appointment');
const offices = document.querySelector('.offices');
const officeAll = document.querySelectorAll('.office');
const roomsAll = document.querySelectorAll('.rooms');
const monthsAll = document.querySelectorAll('.months');

const months = document.querySelectorAll('.month__button');
const breadcrumb = document.querySelector('.breadcrumb');
const persona = document.querySelector('.persona');

const buttonBack = document.getElementById('button-back');

const breadcrumbButtonOffice = document.getElementById('breadcrumb-button-office');
const breadcrumbButtonRoom = document.getElementById('breadcrumb-button-room');
const breadcrumbButtonMonth = document.getElementById('breadcrumb-button-month');
const breadcrumbButtonDay = document.getElementById('breadcrumb-button-day');
const breadcrumbButtonTime = document.getElementById('breadcrumb-button-time');
const breadcrumbButtonPrint = document.getElementById('breadcrumb-button-print');


const stackBack = [];
const ticket = []

function clearActive(element) {
  const elementsSearch = element.querySelectorAll('.active');
  elementsSearch.forEach(elementActive => elementActive.classList.remove('active'));
};

officeAll.forEach(office => {
  const button = office.querySelector('.office__button');    
  button.addEventListener('click', function() {
    this.disabled = true;
    // office.forEach(office => {
    //   office.classList.remove('office-active');
    // });
    breadcrumbButtonOffice.innerHTML = this.innerHTML;
    ticket.push(this.innerHTML);
    
    clearActive(office);

    office.classList.add('active');
    appointment.classList.add('active');

    // breadcrumbButtonOffice.onclick = button.onclick;

    stackBack.push(button);

    buttonBack.value = 1;

    this.disabled = false;
  });
});

roomsAll.forEach(rooms => {
  const roomAll = rooms.querySelectorAll('.room');
  roomAll.forEach(room => {
    const button = room.querySelector('.room__button');
    const span = button.querySelector('span');

    button.addEventListener('click', function() {
      this.disabled = true;
      // rooms.forEach(elem => {
      //   elem.classList.remove('room-active');
      // })
      breadcrumbButtonRoom.innerHTML = span.innerHTML;
      ticket.push(span.innerHTML);
      // breadcrumbButtonRoom.onclick = button.onclick;
      clearActive(room);

      room.classList.add('active');
      rooms.classList.add('active');

      stackBack.push(button);

      buttonBack.value = 2;

      this.disabled = false;
    })
  })
})

monthsAll.forEach(months => {
  const message = months.querySelector('.message');
  const days = months.querySelector('.days');
  const monthButtons = months.querySelectorAll('.month__button');
  monthButtons.forEach(button => {
    button.addEventListener('click', function() {
      this.disabled = true;

      if (document.f_10_02_2_1.num_130.value == 0) {
        //alert('Зарегистрируйтесь указав свой логин и ПИН');
        message.classList.add('active');
        document.f_10_02_2_1.snum_.focus();
        this.disabled = false;
        return
      };
      message.classList.remove('active');

      breadcrumbButtonMonth.innerHTML = button.value;
      ticket.push(button.value);

      clearActive(months);

      // monthButtons.classList.add('active');
      months.classList.add('active');
      days.innerHTML = '';  
      
      // breadcrumbButtonMonth.onclick = month.onclick;

      stackBack.push(button);

      buttonBack.value = 3;
      
      this.disabled = false;
    })

  })
})

function dayActive(event) {
  event.disabled = true;
  const daysWrapper = document.querySelector('.days__wrapper');
  const dayAll = daysWrapper.querySelectorAll('.day');
  // dayAll.forEach(day => {
  //   day.classList.remove('day-active');
  // });
  
  const dayNumber = event.querySelector('.number').innerHTML;
  const dayWeek = event.querySelector('.week').innerHTML;
  breadcrumbButtonDay.innerHTML = dayNumber + ' ' + dayWeek;
  ticket.push(dayNumber + ' ' + dayWeek);
  // breadcrumbButtonDay.onclick = event.onclick;
  
  clearActive(daysWrapper);

  event.parentElement.classList.add('active');
  daysWrapper.classList.add('active');

  stackBack.push(event);

  buttonBack.value = 4;

  event.disabled = false;
}

function timeActive(event) {
  event.disabled = true;
  const times = event.parentElement;
  const timeAll = times.querySelectorAll('.day');
  console.log(times);
  console.log(event);

  // dayAll.forEach(day => {
  //   day.classList.remove('day-active');
  // });
  
  // const dayNumber = event.querySelector('.number').innerHTML;
  // const dayWeek = event.querySelector('.week').innerHTML;
  // breadcrumbButtonDay.innerHTML = dayNumber + ' ' + dayWeek;
  // breadcrumbButtonDay.onclick = event.onclick;
  
  clearActive(times);

  times.classList.add('active');
  event.classList.add('active');

  stackBack.push(event);

  buttonBack.value = 5;

  event.disabled = false;
}


function couponGenerated(value, nVid_, nGr_l, nNum_, sTarget_, sAddn_, sAction_) {
  breadcrumbButtonTime.innerHTML = value;
  ticket.push(value);
  console.log(ticket);
  console.log(stackBack);

  breadcrumbButtonPrint.onclick = () => {
    jsa_031(nVid_, nGr_l, nNum_, sTarget_, sAddn_, sAction_);
  }
}

function js_11_81_1(sIn_) {
  if (document.f_10_02_2_1.num_130.value == 0) {
   //alert('Зарегистрируйтесь указав свой логин и ПИН');
   document.f_10_02_2_1.snum_.focus();
   return
  }
  jsa_031(5,530,11,'saveblank1',sIn_,'is10_08');
 }

 function js_11_81_4() {
  sTmp = document.f_10_02_2_1.snum_.value;
  if (sTmp.length != 16) {
    alert('Укажите номер карточки');
    document.f_10_02_2_1.snum_.focus();
    return
  }
  jsa_031(5,530,17,'saveblank1','','is10_08');
 }
