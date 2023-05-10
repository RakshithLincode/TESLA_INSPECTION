import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { retry, catchError, map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { livisConfig } from "../../config/constants";
import { HerrorService } from "./herror.service"
import { StorageService } from '../helpers/storage.service';

const environment = "development";
const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
let httpOptions = {};

@Injectable({
  providedIn: 'root'
})
export class PmodelService {


  constructor(private http: HttpClient,
    private hErrorService: HerrorService,
    private storageService: StorageService) {
    if (this.storageService.getUserDetails() && this.storageService.getUserDetails().token) {
      const token = this.storageService.getUserDetails().token;
      httpOptions = {
        headers: {
          Authorization: `Token ${token}`,
        },
      };
    }
   }

  getModels(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'parts/get_all_parts/', httpOptions)
      .pipe(map(data => {
        // console.log(data);
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getBulk(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'inspection/get_master_file/', {})
      .pipe(map(data => {
        // console.log(data);
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );
  }

  postFile(fileToUpload: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', fileToUpload);
    return this.http.post<any>(baseUrl + 'inspection/update_file/', formData, httpOptions)
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );

  }


  getModel(id): Observable<any> {
    return this.http.get<{}>(baseUrl + 'cataler/part/' + id, {})
      .pipe(map(data => {
        // console.log(data);
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );
  }

  //add workstation

  addModel(model_info): Observable<any> {
    return this.http.post<any>(baseUrl + 'parts/add_part/', JSON.stringify(model_info), httpOptions)
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );

  }

  updateModel(model_info): Observable<any> {
    return this.http.get<any>(baseUrl + 'parts/part_details/'+ model_info , httpOptions)
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );

  }

  deleteModel(model_info): Observable<any> {
    return this.http.post<any>(baseUrl + 'parts/delete_part/', JSON.stringify(model_info), httpOptions)
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );

  }

  
  submitModel(model_info): Observable<any> {
    console.log(model_info);
    
    return this.http.patch<any>(baseUrl + 'parts/update_part/', JSON.stringify(model_info), httpOptions)
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );

  }


}


