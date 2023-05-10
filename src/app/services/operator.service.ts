import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { retry, catchError, map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { livisConfig } from '../../config/constants';
import { HerrorService } from './herror.service';
const environment = 'development';
import { Router } from '@angular/router';
import { StorageService } from '../helpers/storage.service';

const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
// const baseUrl = 'http://10.60.60.210:8000/main_logic/';
let httpOptions = {

};

@Injectable({
  providedIn: 'root',
})
export class OperatorService {
  isPrinting = false;
  constructor(
    private http: HttpClient,
    private hErrorService: HerrorService,
    private router: Router,
    private storageService: StorageService
  ) {
    const token = this.storageService.getUserDetails().token;
    // //console.log("TOKEN IN CONSTR", token);
    httpOptions = {
      "Content-Type": "application/json",
      headers: {
        Authorization: `Token ${token}`,
      },
    };
  }

  startProcess(start_info): Observable<any> {
    //console.log(start_info)
    return this.http
      .post<{}>(baseUrl + 'inspection/start_process/', start_info, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  startInspection(start_info): Observable<any> {
    //console.log(start_info)
    return this.http
      .post<{}>(baseUrl + 'inspection/start_inspection/', start_info, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );

  }
   submitCapture(start_info): Observable<any> {
    //console.log(start_info)
    return this.http
      .post<{}>(baseUrl + 'inspection/submit/', start_info, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  endProcess(end_info): Observable<any> {
    return this.http
      .post<{}>(baseUrl + 'inspection/end_process/', end_info, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  updateInspectionQc(inspection_info) {
    return this.http
      .post<{}>(
        baseUrl + 'toyoda/update_manual_qc/',
        inspection_info,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getRunningProcess(): Observable<any> {
    return this.http
      .get<{}>(
        baseUrl + 'inspection/get_running_process/',
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getAllParts(): Observable<any> {
    //console.log("TOKEN IN CONSTR", httpOptions);

    return this.http
      .get<{}>(
        baseUrl + 'parts/get_all_parts/', httpOptions
      )

      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }
  getInspection(payload: any): Observable<any> {

    return this.http
      .post<{}>(
        baseUrl + 'inspection/get_ui_trigger/', payload
      )

      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }
  setConfig(payload:any): Observable<any> {

    return this.http
    .post<{}>(
      baseUrl + 'set_config/',payload
      )
     
    .pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }
  

  setThreshold(payload:any): Observable<any> {

    return this.http
    .post<{}>(
      baseUrl + 'inspection/set_config/',payload
      )
     
    .pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  rescanProcess(rescan_onfo) {
    return this.http
      .post<{}>(baseUrl + 'toyoda/update_manual_qc/', rescan_onfo, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getMetrix(id): Observable<any> {
    return this.http
      .get<{}>(baseUrl + 'inspection/getDefectList/' + id + '/', httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getDefectList(inspection_id): Observable<any> {
    return this.http
      .get<{}>(
        baseUrl + 'reports/get_defect_list/' + inspection_id,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getCameraFeed(): Observable<any> {
    return this.http
      .get<{}>(baseUrl + 'inspection/get_capture_feed_url/', httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getProcessSummary(process_id): Observable<any> {
    return this.http
      .get<{}>(baseUrl + 'reports/getSummary/' + process_id, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  modifyPlannedProduction(product_info): Observable<any> {
    return this.http
      .post<{}>(
        baseUrl + 'inspection/plan_production_counter_modify/',
        product_info,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  printDocument(process_id) {
    this.isPrinting = true;
    this.router.navigate(['/operator/print'], {
      queryParams: { process_id: process_id },
    });
  }

  onDataReady() {
    setTimeout(() => {
      window.print();
      this.isPrinting = false;
      this.router.navigate(['operator']);
    });
  }

  getQrCode() {
    return this.http
      .get<{}>(baseUrl + 'toyoda/generate_QRcode/', httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  camToPart() {
    return this.http.post(baseUrl + 'cam_to_part/', httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }
}
