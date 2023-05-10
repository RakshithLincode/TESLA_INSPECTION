import { Injectable } from '@angular/core';
import {throwError } from 'rxjs';
import {AlertService} from "../services/alert.service";

@Injectable({
  providedIn: 'root'
})
export class HerrorService {
  hErrorService:any;
  constructor(private alertNotification:AlertService)
   {

    }

  handleError(error) {

    let errorMessage = '';
 
    if (error.error instanceof ErrorEvent) {
 
      // client-side error
 
      errorMessage = `Error: ${error.error.message}`;
 
    } else {
 
      // server-side error
 
      errorMessage = error.error.message;
 
    }
    // console.log(error.error.message);
    // console.log(this);
    // console.log(error);
    // window.alert(errorMessage);
    // this.alertNotification.error("dd");
    // localStorage.setItem('user', "{token:123367}");
    if(errorMessage){
      this.hErrorService.alertNotification.alertMessage(errorMessage,'danger','error')
    }else{
      this.hErrorService.alertNotification.alertMessage("Unknown Error",'danger','error')
    }
 
    return throwError(errorMessage);
 
  }
}
