import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  constructor() 
  { 
    
  }
  getUserDetails()
  {
    // console.log(JSON.parse(localStorage.getItem('user')));
    return JSON.parse(localStorage.getItem('livis_user'));
    // if(localStorage.getItem('user'))
    // {
    //   this.router.navigate(['dashboard']);
    // }
  }

}
