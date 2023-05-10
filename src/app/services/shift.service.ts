import { Injectable } from '@angular/core';
import { Observable, from} from 'rxjs';
import { retry, catchError,map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {livisConfig} from "../../config/constants";
import {HerrorService} from "./herror.service"
const environment =  "development";
const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
// const baseUrl = "http://164.52.194.78:8000/livis/";
const httpOptions = {};

@Injectable({
  providedIn: 'root'
})
export class ShiftService {

  constructor(private http: HttpClient,private hErrorService: HerrorService) { }

  getShifts(): Observable<any> {
    return this.http.get<{}>(baseUrl+'cataler/get_shifts/',{})
    .pipe(map(data => {
      console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  getShift(id): Observable<any> {
    return this.http.get<{}>(baseUrl+'cataler/get_shift/'+id,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  //add shift

  addShift(shift_info): Observable<any> {
    
    return this.http.post<any>(baseUrl+'cataler/add_shift/', JSON.stringify(shift_info), httpOptions)
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  updateShift(shift_info): Observable<any> {
    
    return this.http.post<any>(baseUrl+'cataler/update_shift/', JSON.stringify(shift_info), httpOptions)
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  deleteShift(shift_id): Observable<any> {
    
    return this.http.delete<any>(baseUrl+'cataler/delete_shift/'+shift_id, httpOptions)
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }


}
