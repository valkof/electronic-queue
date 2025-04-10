const appointment = document.querySelector('.appointment');
const offices = document.querySelector('.offices');
const officeAll = document.querySelectorAll('.office');
const roomsAll = document.querySelectorAll('.rooms');
const monthsAll = document.querySelectorAll('.months');

const months = document.querySelectorAll('.month__button');
const breadcrumb = document.querySelector('.breadcrumb');
const persona = document.querySelector('.persona');
const userId = document.getElementById("user-id");

const buttonStart = document.getElementById('button-start');
const buttonBack = document.getElementById('button-back');
const currentTime = document.getElementById('current-time');
const currentDate = document.getElementById('current-date');
const buttonNewTicket = document.getElementById('button-new-ticket');

const modalPrint = document.getElementById('modal__print');
const buttonPrintOk = document.getElementById('print-yes');
const modalMsg = document.getElementById('modal__msg');
const modalText = document.getElementById('modal__msg-content');
const modalContinue = document.getElementById('modal__continue');

const breadcrumbButtonOffice = document.getElementById('breadcrumb-button-office');
const breadcrumbButtonRoom = document.getElementById('breadcrumb-button-room');
const breadcrumbButtonMonth = document.getElementById('breadcrumb-button-month');
const breadcrumbButtonDay = document.getElementById('breadcrumb-button-day');
const breadcrumbButtonTime = document.getElementById('breadcrumb-button-time');
const breadcrumbButtonPrint = document.getElementById('breadcrumb-button-print');
const ticketElements = [buttonStart, breadcrumbButtonOffice, breadcrumbButtonRoom, breadcrumbButtonMonth, breadcrumbButtonDay, breadcrumbButtonTime];

let timerSeance = 0;
let timerSeanceMax = 35;
const ticket = [''];
const stackBack = [buttonStart];

document.documentElement.setAttribute('lang', 'ru');

function focusOnUserId() {
  console.log('ok');
  userId.focus();
};

const focusId = setInterval(focusOnUserId, 500);

function currentDateTime() {
  const datetime = new Date();
  const date = datetime.toLocaleDateString('ru', {
    month: "long",
    day: "2-digit"
  });
  const time = datetime.toLocaleTimeString('ru', {
    hour: "2-digit",
    minute: "2-digit"
  });
  currentTime.innerText = time;
  currentDate.innerText = date;
  timerSeance += 5;  // создать функцию
  // if (timerSeance == timerSeanceMax) {
  //   modalContinue.classList.add('active');
  // }
};

currentDateTime();
setInterval(currentDateTime, 5000);

document.forms.f_10_02_2_1.addEventListener('submit', event => {
	js_11_81_4();
  clearInterval(focusId);
  const message = document.querySelector('.message.active');
  if (message) message.classList.remove('active');
  console.log('я выполнилась и удалилась');
  buttonNewTicket.value = 1;
	event.preventDefault();
}, {once: true});

function stepBack() {
  ticket.pop();
  ticket.pop();
  stackBack.pop();
  const element = stackBack.pop();
  element.click();
}

function setTicketCaption() {
  ticketElements.forEach((element, num) => {
    element.innerHTML = ticket[num] || '';
  })
}

function clearActive(element) {
  const elementsSearch = element.querySelectorAll('.active');
  elementsSearch.forEach(elementActive => elementActive.classList.remove('active'));
};

function openStartScreen(event) {
  event.disabled = true;

  ticket.push('');
  setTicketCaption();

  clearActive(appointment);
  appointment.classList.remove('active');

  stackBack.push(event);

  buttonBack.value = 0;
  breadcrumbButtonPrint.value = 0;

  event.disabled = false;
};

function newTicket() {
  document.f_10_02_2_1.submit();
}

officeAll.forEach(office => {
  const button = office.querySelector('.office__button');    
  button.addEventListener('click', function() {
    this.disabled = true;

    ticket.push(this.innerHTML);
    setTicketCaption();
    
    clearActive(office);

    office.classList.add('active');
    appointment.classList.add('active');

    stackBack.push(button);

    buttonBack.value = 1;
    breadcrumbButtonPrint.value = 0;

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

      ticket.push(span.innerHTML);
      setTicketCaption();

      clearActive(room);

      room.classList.add('active');
      rooms.classList.add('active');

      stackBack.push(button);

      buttonBack.value = 2;
      breadcrumbButtonPrint.value = 0;

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

      ticket.push(button.value);
      setTicketCaption();

      clearActive(months);

      months.classList.add('active');
      days.innerHTML = '';  

      stackBack.push(button);

      buttonBack.value = 3;
      breadcrumbButtonPrint.value = 0;
      
      this.disabled = false;
    })

  })
})

function dayActive(event) {
  event.disabled = true;
  // const daysWrapper = document.querySelector('.days__wrapper');
  const daysWrapper = event.parentElement.parentElement;
  console.log(daysWrapper);
  const dayAll = daysWrapper.querySelectorAll('.day');
  
  const dayNumber = event.querySelector('.number').innerHTML;
  const dayWeek = event.querySelector('.week').innerHTML;
  ticket.push(dayNumber + ' ' + dayWeek);
  setTicketCaption();
  
  clearActive(daysWrapper);

  event.parentElement.classList.add('active');
  daysWrapper.classList.add('active');

  stackBack.push(event);

  buttonBack.value = 4;
  breadcrumbButtonPrint.value = 0;

  event.disabled = false;
}

function timeActive(event) {
  event.disabled = true;
  const times = event.parentElement;
  const timeAll = times.querySelectorAll('.day');

  ticket.push(event.value);
  setTicketCaption();
  
  clearActive(times);

  times.classList.add('active');
  event.classList.add('active');

  stackBack.push(event);

  buttonBack.value = 5;
  breadcrumbButtonPrint.value = 1;

  event.disabled = false;
}


function couponGenerated(nVid_, nGr_l, nNum_, sTarget_, sAddn_, sAction_) {
  buttonPrintOk.onclick = function(event) {
    event.target.disabled = true;
    const fio = document.getElementById('name-patient');
    ticket[0] = fio.value;
    sAddn_ += ',' + ticket.join(','); 
    console.log(sAddn_);
    jsa_031(nVid_, nGr_l, nNum_, sTarget_, sAddn_, sAction_);
  }
}

function openModalPrint() {
  modalPrint.classList.add('active');
};

function closeModalPrint() {
  modalPrint.classList.remove('active');
};

function openModalMsg() {
  modalMsg.classList.add('active');
}

function closeModalContinue() {

};

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
