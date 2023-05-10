import { Injectable } from '@angular/core';
import { Observable, from,} from 'rxjs';
import { retry, catchError,map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {livisConfig} from "../../config/constants";
import {HerrorService} from "./herror.service"
const environment =  "development";
const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
const httpOptions = {};
@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor( private http: HttpClient,private hErrorService: HerrorService) {

   }

  getWorkStations():Observable<{}> {

    return this.http.get<{}>(baseUrl+'workstations/get_workstations/')
    // console.log(baseUrl+'accounts/api/v1/login');
    // return of([
    //   {value: '1', viewValue: 'Workstatation1'},
    //   {value: '1', viewValue: 'Workstatation2'},
    //   {value: '1', viewValue: 'Workstatation3'},
    // ]);
  }

  userLogin(email,password): Observable<{}> {
    return this.http.post<{}>(baseUrl+'accounts/login/', {email:email,password:password}, httpOptions)
    .pipe(map(user_info => {
      // user_info['workstation_id'] = workstation_name;
      // user_info['name'] = "Shyam";
      // user_info['role'] = "System Admin";
      // user_info['user_id'] = "5ef5005a-5473-440b-ab29-272a810da5d3";


      // window.Data1 = 
      // gwindow.$livis_user_info = 
      // store user details and jwt token in local storage to keep user logged in between page refreshes
      const logoImages = JSON.parse(localStorage.getItem('livis_user'));
      user_info = {...user_info, ...logoImages};
      localStorage.setItem('livis_user', JSON.stringify(user_info));
      this.setCookie('livis_user', JSON.stringify(user_info), 365);
      // localStorage.setItem('workstation_id', workstation_name);
      return user_info;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  adminLogin(email,password): Observable<{}> {
    return this.http.post<{}>(baseUrl+'accounts/login/', {email:email,password:password,workstation_name:"dd"}, httpOptions)
    .pipe(map(user_info => {
      // user_info['workstation_id'] = workstation_name;
      // user_info['name'] = "Shyam";
      // user_info['role'] = "System Admin";
      // user_info['user_id'] = "5ef5005a-5473-440b-ab29-272a810da5d3";
      // store user details and jwt token in local storage to keep user logged in between page refreshes
      if(user_info['role_name'] == 'sys admin'){
        // alert("hi");
        localStorage.setItem('user', JSON.stringify(user_info));
      }
      // localStorage.setItem('workstation_id', workstation_name);
      return user_info;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  checkUserLogin(email,password,workstation_name): Observable<{}> {
    return this.http.post<{}>(baseUrl+'accounts/login/', {email:email,password:password,workstation_name:workstation_name}, httpOptions)
    .pipe(map(user_info => {
      return user_info;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }


logout() {
    localStorage.removeItem('user');
    this.removeCookie('livis_user');
}

setCookie(name, value, days) {
  let expires = '';
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = '; expires=' + date.toUTCString();
  }
  document.cookie = name + '=' + (value || '') + expires + '; path=/';
}

getCookie(name) {
  const nameEQ = name + '=';
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1, c.length);
    }
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

removeCookie(name) {
  console.log('before', this.getCookie(name));
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
  console.log('after', this.getCookie(name));
}

getLogoImages(): Observable<any> {
  return this.http
    .get<any>(baseUrl + 'assects/get_assect/')
    .pipe(
      map((data) => {
        localStorage.setItem('user', JSON.stringify(data));
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
}

  
 
 


}
