var newMemberAddBtn = document.querySelector('.addMemberBtn'),
    addmember = document.querySelector('.addmember--content'),
    popupForm = document.querySelector('.popup'),
    crossBtn = document.querySelector('.closeBtn'),
    submitBtn = document.querySelector('.submitBtn'),
    modalTitle = document.querySelector('.modalTitle'),
    popupFooter = document.querySelector('.popupFooter'),
    form = document.querySelector('form'),
    username = document.getElementById("username"),
    fName = document.getElementById("fName"),
    lName = document.getElementById("lName"),
    email = document.getElementById("email"),
    dateJoined = document.getElementById("dateJoined"),
    isStaff = document.getElementById("isStaff");

newMemberAddBtn.addEventListener('click', ()=> {
    submitBtn.innerHTML = "Submit";
    modalTitle.innerHTML = "Fill the Form";
    popupFooter.style.display = "block";
    addmember.classList.add('active');
    popupForm.classList.add('active');
});

crossBtn.addEventListener('click', ()=>{
    addmember.classList.remove('active');
    popupForm.classList.remove('active');
    form.reset();
});


