import { Injectable } from '@angular/core';
import { Observable, from, of } from 'rxjs';
import { retry, catchError, map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { livisConfig } from '../../config/constants';
import { HerrorService } from './herror.service';
const environment = 'development';
import { Router } from '@angular/router';
import { StorageService } from '../helpers/storage.service';

const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
// const baseUrl = 'http://10.60.60.78:8000/main_logic/';
let httpOptions = {};

@Injectable({
  providedIn: 'root',
})
export class MarutiOperatorService {
  constructor(
    private http: HttpClient,
    private hErrorService: HerrorService,
    private storageService: StorageService
  ) {
    const token = this.storageService.getUserDetails().token;
    httpOptions = {
      headers: {
        Authorization: `Token ${token}`,
      },
    };
  }

  getData(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'getData', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getSealentMin(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'SealentWidthMin', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getSealentMax(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'SealentWidthMax', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getFlangeMin(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'FlangeWidthMin', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getFlangeMax(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'FlangeWidthMax', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getMetrix(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'get_metrics', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  edit(payload): Observable<any> {
    return this.http
      .post<{}>(baseUrl + 'set_min_sealant_width', payload, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  startProcess(start_info): Observable<any> {
    return this.http
      .post<{}>(baseUrl + 'indo/start_process/', start_info, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
    // let data = {
    //   Message: "Success"
    // }
    // return of(data);
  }

  endProcess(end_info): Observable<any> {
    // return this.http
    //   .post<{}>(baseUrl + 'inspection/end_inspection/', end_info, httpOptions)
    //   .pipe(
    //     map((data) => {
    //       return data;
    //     }),
    //     catchError(this.hErrorService.handleError.bind(this))
    //   );
    let data = {
      Message: "Success"
    }

    return of(data);
  }

  getRunningProcess(): Observable<any> {
    return this.http
      .get<{}>(baseUrl + 'indo/get_running_process', httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
    // let data = {
    //   part_name: 'M7',
    //   part_id: 'M7-7846',
    //   inspection_id: '3784bfdhrjgfd4764dfj'
    // }
    // return of(data);
  }

  result(): Observable<any> {
    return this.http.post<{}>(baseUrl + 'acceptandrejection', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }
}
