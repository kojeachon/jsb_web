// console.log("Hello world!!")

  
$(function () {
  // //Datemask dd/mm/yyyy
  // $('#datemask').inputmask('dd/mm/yyyy', { 'placeholder': 'dd/mm/yyyy' })
  // //Datemask2 mm/dd/yyyy
  // $('#datemask2').inputmask('mm/dd/yyyy', { 'placeholder': 'mm/dd/yyyy' })
  // //Money Euro
  // $('[data-mask]').inputmask()

  //Start Date picker
  $('#st_date').datetimepicker({
    // dateFormat: 'yy-mm-dd',
    format: 'L'
      // format: 'YYYY-MM-DD'
  });

  //End Date picker
  $('#ed_date').datetimepicker({
    // dateFormat: 'yy-mm-dd',
    format: 'L'
    // format: 'YYYY-MM-DD'
  });

  // //Date and time picker
  // $('#reservationdatetime').datetimepicker({ icons: { time: 'far fa-clock' } });

  // //Date range picker
  // $('#reservation').daterangepicker()
  // //Date range picker with time picker
  // $('#reservationtime').daterangepicker({
  //   timePicker: true,
  //   timePickerIncrement: 30,
  //   locale: {
  //     format: 'MM/DD/YYYY hh:mm A'
  //   }
  // })
  // //Date range as a button
  // $('#daterange-btn').daterangepicker(
  //   {
  //     ranges   : {
  //       'Today'       : [moment(), moment()],
  //       'Yesterday'   : [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
  //       'Last 7 Days' : [moment().subtract(6, 'days'), moment()],
  //       'Last 30 Days': [moment().subtract(29, 'days'), moment()],
  //       'This Month'  : [moment().startOf('month'), moment().endOf('month')],
  //       'Last Month'  : [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
  //     },
  //     startDate: moment().subtract(29, 'days'),
  //     endDate  : moment()
  //   },
  //   function (start, end) {
  //     $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'))
  //   }
  // )

  // //Timepicker
  // $('#timepicker').datetimepicker({
  //   format: 'LT'
  // })

  const type1select = document.getElementById('type1')
  const type2select = document.getElementById('type2')
  const roomnumberselect = document.getElementById('roomnumber')
  const roommoneyinput = document.getElementById('roommoney')
  const alertBox = document.getElementById('alert-box')
  const csrf = document.getElementsByName('csrfmiddlewaretoken')

  $.ajax({
    type: 'GET',
    url: '/leases/type1-json/',
    success: function(response){
        const type1Data = response.data
        // console.log(type1Data)
        type1Data.forEach(element => {
          const type1option = document.createElement('option')
          type1option.text = element.type1
          type1option.setAttribute('value', element.type1)
          type1select.appendChild(type1option)
          // console.log(element.type1)
        });
    },
    error: function(error){
        console.log(error)
    }
  })


  type1select.addEventListener('change', e=>{
    // console.log(e.target.value)
    const selectedtype1 = e.target.value

    // alertBox.innerHTML=""
    type2select.innerHTML = ""
    const type2option = document.createElement('option')
    type2option.text = "선택"
    type2option.setAttribute('selected','')
    type2select.appendChild(type2option)


    $.ajax({
        type: 'GET',
        url: `/leases/type2-json/${selectedtype1}/`,
        success: function(response){
            console.log(response.data)
            const type2Data = response.data
            type2Data.forEach(element => {
              const type2option = document.createElement('option')
              type2option.text = element.type2
              type2option.setAttribute('value', element.type2)
              type2select.appendChild(type2option)
              // console.log(element.type2)
            });
        },
        error: function(error){
            console.log(error)
        }
    })
  })

  var dictObject = {}
  type2select.addEventListener('change', e=>{
    // console.log(e.target.value)
    const selectedtype2 = e.target.value

    // alertBox.innerHTML=""
    roomnumberselect.innerHTML = ""
    const roomnumberoption = document.createElement('option')
    roomnumberoption.text = "선택"
    roomnumberoption.setAttribute('selected','')
    roomnumberselect.appendChild(roomnumberoption)
    roommoneyinput.value = ""

    $.ajax({
        type: 'GET',
        url: `/leases/roomnumber-json/${selectedtype2}/`,
        success: function(response){
            console.log(response.data)
            const roomnumberData = response.data
            roomnumberData.forEach(element => {
              const roomnumberoption = document.createElement('option')
              roomnumberoption.text = element.roomnumber
              roomnumberoption.setAttribute('value', element.roomnumber)
              roomnumberselect.appendChild(roomnumberoption)
              dictObject[element.roomnumber] = element.roommoney
              // console.log(element.roomnumber,element.roommoney)
            });

            // modelInput.addEventListener('change', e=>{
            //     btnBox.classList.remove('not-visible')
            // })
        },
        error: function(error){
            console.log(error)
        }
    })
  })

  roomnumberselect.addEventListener('change', e=>{
    console.log(e.target.value,dictObject[e.target.value])
    roommoneyinput.value = dictObject[e.target.value]
  })
  
  // $("#leaseForm").submit(function(e){
  //   e.preventDefault()
  //   console.log('submitted',$("#st_date").val())
  // })
  leaseForm.addEventListener('submit', e=>{
    e.preventDefault()
    $.ajax({
      type: 'POST',
      url: '/leases/save-lease-create/',
      data: {
          'csrfmiddlewaretoken': csrf[0].value,
          'st_date':$("#st_date").val(),
          'ed_date':$("#ed_date").val(),
          'type1':$("#type1").val(),
          'type2':$("#type2").val(),
          'roomnumber':$("#roomnumber").val(),
          'usepeople':$("#usepeople").val(),
          'leasename':$("#leasename").val(),
          'phonenumber':$("#phonenumber").val(),
          'contents':$("#contents").val(),
      },
      success: function(response){
          console.log(response)
          alertBox.innerHTML = `<div class="ui positive message">
                                  <div class="header">
                                  Success
                                  </div>
                                  <p>Your order has been placed</p>
                              </div>`
          $(location).attr('href', '/leases')
      },
      error: function(error){
          console.log(error)
          alertBox.innerHTML = `<div class="ui negative message">
                                  <div class="header">
                                  Ops
                                  </div>
                                  <p>Something went wrong</p>
                              </div>`
      }
    })
  })




  $.validator.setDefaults({
    submitHandler: function () {
      alert( "Form successful submitted!" );
    }
  });
  $('#leaseForm').validate({
    rules: {
      st_date: {
        required: true,
      },
      ed_date: {
        required: true,
      },
      type1: {
        required: true,
      },
      type2: {
        required: true,
      },
      roomnumber: {
        required: true,
      },
      roommoney: {
        required: true,
      },
      usepeople: {
        required: true,
      },
      leasename: {
        required: true,
      },
      phonenumber: {
        required: true
      },
    },
    messages: {
      email: {
        required: "Please enter a email address",
        email: "Please enter a vaild email address"
      },
      password: {
        required: "Please provide a password",
        minlength: "Your password must be at least 5 characters long"
      },
      terms: "Please accept our terms"
    },
    errorElement: 'span',
    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');
      element.closest('.form-group').append(error);
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass('is-invalid');
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).removeClass('is-invalid');
    }
  });




})
