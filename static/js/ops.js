
function notify(type,icon,msg){

  $.notify({
      // options
      icon: icon,
      title: '<b>Ops+提示:</b>',
      message: msg,
    },{
      allow_dismiss: true,
      newest_on_top: false,
      type: type,
      delay: 5000,
      timer: 1000,
      icon_type: 'class',
      template: '<div data-notify="container" class="col-xs-11 col-sm-2 alert alert-{0}" role="alert">' +
        '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
        '<span data-notify="icon"></span> ' +
        '<span data-notify="title">{1}</span> ' +
        '<span data-notify="message">{2}</span>' +
        '<div class="progress" data-notify="progressbar">' +
          '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
        '</div>'+
      '</div>' 
    });

}
