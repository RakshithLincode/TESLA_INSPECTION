import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {AlertService} from '../../services/alert.service'

@Component({
  selector: 'app-livis-logout',
  templateUrl: './livis-logout.component.html',
  styleUrls: ['./livis-logout.component.css']
})
export class LivisLogoutComponent implements OnInit {

  constructor(private router: Router,
    private alertService:AlertService) { }

  ngOnInit(): void {
    localStorage.removeItem('livis_user');
    localStorage.removeItem('livis_user_permissions');
    this.alertService.alertMessage("Logout Successfully","success","check");
    this.router.navigate(['']);
  }

}
