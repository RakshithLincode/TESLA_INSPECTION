import { Injectable } from '@angular/core';
import { Observable, from} from 'rxjs';
import { retry, catchError,map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {livisConfig} from "../../config/constants";
import {HerrorService} from "./herror.service"
import { StorageService } from '../helpers/storage.service';

const environment =  "development";
const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
let httpOptions = {};

@Injectable({
  providedIn: 'root'
})
export class DefectreportService {

  constructor(private http: HttpClient,private hErrorService: HerrorService, 
    private storageService: StorageService) {
    const token = this.storageService.getUserDetails().token;
    // //console.log("TOKEN IN CONSTR", token);
    httpOptions = {
      "Content-Type" : "application/json",
      headers: {
        Authorization: `Token ${token}`,
      },
    };
  
   }

  getDefectReport(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'reports/getMegaReport/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  downloadReport(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl+'reports/exportCSV/', JSON.stringify(report_filter), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }




  getMasterDefectList(): Observable<any> {
    return this.http.get<{}>(baseUrl+'cataler/get_master_defect_list/',{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getMasterFeatureList(): Observable<any> {
    return this.http.get<{}>(baseUrl+'cataler/get_master_feature_list/',{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }


}
