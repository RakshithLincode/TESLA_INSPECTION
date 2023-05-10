import { Injectable } from '@angular/core';
declare const $: any;
@Injectable({
  providedIn: 'root'
})
export class AlertService {
// icon;
  constructor() { 
    // this.icon = null;
  }

// icon=null;

// mytemplate = 
    // const type = ['', 'info', 'success', 'warning', 'danger', 'rose', 'primary'];
  alertMessage(message: string,color:string,icon:string) {
    $.notify({
        icon: icon,
        message: message
    }, {
        type: color,
        timer: 3000,
        placement: {
            from: "top",
            align: "right"
        },
        template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0} alert-with-icon" role="alert">' +
        '<button mat-raised-button type="button" aria-hidden="true" class="close" data-notify="dismiss">  <i class="material-icons">close</i></button>' +
        '<i class="material-icons" data-notify="icon">'+icon+'</i> ' +
        '<span data-notify="title">{1}</span> ' +
        '<span data-notify="message">{2}</span>' +
        '<div class="progress" data-notify="progressbar">' +
          '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
        '</div>' +
        '<a href="{3}" target="{4}" data-notify="url"></a>' +
        '</div>'
    });
  }


  // successMessage(message: string) {
  //   this.icon = "check";
  //   $.notify({
  //       icon: 'check',
  //       message: message
  //   }, {
  //       type: 'success',
  //       timer: 3000,
  //       placement: {
  //           from: "top",
  //           align: "right"
  //       },
  //       template: this.mytemplate
  //   });
  // }

}
