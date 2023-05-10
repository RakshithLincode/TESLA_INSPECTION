import { Injectable } from '@angular/core';
import { CanActivate,Router, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import {StorageService} from "./storage.service";

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  constructor(
    private router: Router,
    private storageService: StorageService
) {}

canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
  
    const UserDetails = this.storageService.getUserDetails();
    // const currentUser = true;
    if (UserDetails && UserDetails['role_name'] === 'admin') {
        // authorised so return true
        return true;
    }

    // not logged in so redirect to login page with the return url
    this.router.navigate(['/operator']);
    return false;
}
  
}
