import { Injectable } from '@angular/core';
import { Observable, from} from 'rxjs';
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
export class ReportService {

  constructor(private http: HttpClient,private hErrorService: HerrorService) { }

  getDefectTypeReports(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'cataler/get_defect_type_summary/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  getDefectTypeDetailsReports(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'cataler/get_defect_details_summary_ind/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  getProductionQualityReports(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'cataler/get_production_quality_summary_ind/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  geOperators(): Observable<any> {
    return this.http.get<any>(baseUrl+'cataler/get_operators/', httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  getShiftReports(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'cataler/get_shift_summary_ind/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  downloadDefectTypeReports(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'cataler/get_defect_type_summary_export/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }
  
  downloadProductionQualityReports(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'cataler/get_production_quality_summary_ind_export/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }


  downloadShiftReports(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'cataler/get_shift_summary_ind_export/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }
  


}
