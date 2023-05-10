import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { StorageService } from '../helpers/storage.service';
import { HerrorService } from './herror.service';
import { livisConfig } from '../../config/constants';

const environment = 'development';


const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
let httpOptions = {};

interface AddNewUserDto {
  username: string;
  firstName: string;
  lastName: string;
  email: string;
  roleName: string;
  password: string;
  confirmPassword: string;
}

interface EditUserDto {
  username: string;
  firstName: string;
  lastName: string;
  email: string;
  roleName: string;
}

export interface UserInfoResponse {
  model: string;
  pk: string;
  fields: {
    last_login: string;
    is_staff: boolean;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    user_address: string;
    date_joined: string;
    updated_at: string;
    is_deleted: boolean;
    is_active: boolean;
    is_superuser: boolean;
    role_name: string;
    phone_number: string;
    groups: [];
    user_permissions: [];
  };
}

@Injectable({
  providedIn: 'root',
})
export class ManageUserService {
  constructor(
    private http: HttpClient,
    private hErrorService: HerrorService,
    private storageService: StorageService
  ) {
    if (this.storageService.getUserDetails() && this.storageService.getUserDetails().token) {
      const token = this.storageService.getUserDetails().token;
      httpOptions = {
        headers: {
          Authorization: `Token ${token}`,
        },
      };
    }
  }

  getAllUsers(): Observable<UserInfoResponse[]> {
    return this.http
      .get<UserInfoResponse[]>(
        baseUrl + 'accounts/user_accounts/',
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getUsers(itemsPerPage: number): Observable<UserInfoResponse[]> {
    return this.http
      .get<UserInfoResponse[]>(
        baseUrl + 'accounts/user_accounts/?page=1&limit=' + itemsPerPage,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  addNewUser(payload: AddNewUserDto): Observable<any> {
    return this.http
      .post<any>(baseUrl + 'accounts/add_user_account/', payload, httpOptions)
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  updateUser(payload: EditUserDto): Observable<any> {
    return this.http
      .patch<any>(
        baseUrl + 'accounts/update_user_account/',
        payload,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  deleteUser(userID: string): Observable<any> {
    return this.http
      .delete<any>(
        baseUrl + 'accounts/delete_user_account/' + userID,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  searchUser(query: string, itemPerPage: number): Observable<any> {
    const URL = `${baseUrl}clients/users?search=${query}&page=1&limit=${itemPerPage}`;

    return this.http.get<any>(URL).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getUser(id: string): Observable<any> {
    return this.http.get<any>(baseUrl + 'accounts/get_user_account/' + id, httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    )
  }

  getFilteredUsers(
    query: string,
    itemsPerPage: number,
    pageNumber: number
  ): Observable<any> {
    let URL = `${baseUrl}accounts/user_accounts/?page=${pageNumber}&limit=${itemsPerPage}`;

    if (query) {
      URL += '&search=' + query;
    }

    return this.http.get<any>(URL, httpOptions).pipe(
      map((data) => {
        return data;
      }),
      catchError(this.hErrorService.handleError.bind(this))
    );
  }
}
