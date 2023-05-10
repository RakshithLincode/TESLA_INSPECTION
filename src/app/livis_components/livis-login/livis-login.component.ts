import { Component, OnInit, ElementRef, OnDestroy, ViewEncapsulation } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { AuthenticationService } from '../../services/authentication.service';
import { Router } from '@angular/router'
import { AlertService } from '../../services/alert.service'
import { from } from 'rxjs';
const environment = 'development';
import { livisConfig } from '../../../config/constants';




declare var $: any;

@Component({
  selector: 'app-livis-login',
  templateUrl: './livis-login-new.component.html',
  styleUrls: ['./livis-login-new.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LivisLoginComponent implements OnInit, OnDestroy {
  loginForm: FormGroup;
  isSubmitted = false;
  currentTab = 'operator';
  logo: string;


  test: Date = new Date();
  private toggleButton: any;
  private sidebarVisible: boolean;
  private nativeElement: Node;
  baseUrl: any;

  constructor(private element: ElementRef,
    private authenticationService: AuthenticationService,
    private formBuilder: FormBuilder,
    private router: Router,
    private alertService: AlertService) {
    const environmentConfig = livisConfig[environment];
    this.baseUrl = environmentConfig.BASE_URL;
    this.nativeElement = element.nativeElement;
    this.sidebarVisible = false;
    if (localStorage.getItem('livis_user')) {
      let user_info = JSON.parse(localStorage.getItem('livis_user'));
      if (user_info && user_info['role_name']) {
        if (user_info['role_name'] == 'admin') {
          this.router.navigate(['report/reports']);
        } else {
          this.router.navigate(['operator']);
        }
      }
    }

    // this.loginForm = formBuilder.group({
    //   email: ['',Validators.required],
    //   password: ['',Validators.required],
    //   workstation_name:['',Validators.required],
    // });
  }




  selectTheme = 'primary';

  workstations: {};
  getWorkStations(): void {
    this.authenticationService.getWorkStations()
      .subscribe(workstations => this.workstations = workstations);
    // this.workstations = this.loginService.getWorkStations();
  }

  // 
  // cities = [
  //   {value: '1', viewValue: 'Workstatation1'},
  //   {value: '1', viewValue: 'Workstatation2'},
  //   {value: '1', viewValue: 'Workstatation3'},


  // ];

  ngOnInit() {

    var navbar: HTMLElement = this.element.nativeElement;
    this.toggleButton = navbar.getElementsByClassName('navbar-toggle')[0];
    const body = document.getElementsByTagName('body')[0];
    body.classList.add('login-page');
    body.classList.add('off-canvas-sidebar');
    const card = document.getElementsByClassName('card')[0];
    // setTimeout(function() {
    // after 1000 ms we add the class animated to the login/register card
    // card.classList.remove('card-hidden');
    // }, 700);
    // this.getWorkStations();
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required]],
      password: ['', Validators.required],
      // workstation_name:['',Validators.required],
    });

    if (!localStorage.getItem('user')) {
      // this.getLogoImages();
    } else {
      this.logo = JSON.parse(localStorage.getItem('user')).login_img;
    }
  }

  sidebarToggle() {
    var toggleButton = this.toggleButton;
    var body = document.getElementsByTagName('body')[0];
    var sidebar = document.getElementsByClassName('navbar-collapse')[0];
    if (this.sidebarVisible == false) {
      setTimeout(function () {
        toggleButton.classList.add('toggled');
      }, 500);
      body.classList.add('nav-open');
      this.sidebarVisible = true;
    } else {
      this.toggleButton.classList.remove('toggled');
      this.sidebarVisible = false;
      body.classList.remove('nav-open');
    }
  }
  ngOnDestroy() {
    const body = document.getElementsByTagName('body')[0];
    body.classList.remove('login-page');
    body.classList.remove('off-canvas-sidebar');
  }

  // validateAllFormFields(formGroup: FormGroup) {
  //   Object.keys(formGroup.controls).forEach(field => {
  //     const control = formGroup.get(field);
  //     if (control instanceof FormControl) {
  //       control.markAsTouched({ onlySelf: true });
  //     } else if (control instanceof FormGroup) {
  //       this.validateAllFormFields(control);
  //     }
  //   });
  // }

  get formControls() {
    return this.loginForm.controls;
  }

  loginAdmin() {
    console.log("admin")
    this.isSubmitted = true;

    if (this.loginForm.invalid) {
      return;
    }

    this.authenticationService
      .userLogin(
        this.loginForm.get('email').value,
        this.loginForm.get('password').value,
        // this.loginForm.get('workstation_name').value,
      )
      .subscribe((response) => {

        if (response['role_name'] === 'admin') {
          this.alertService.alertMessage(
            'Login Successfully',
            'success',
            'check'
          );
          this.router.navigate(['operator']);
        } else {
          this.alertService.alertMessage('Unauthorized', 'danger', 'error');
          localStorage.removeItem('livis_user');
        }
      });
  }

  loginUser(event) {

    console.log(this.loginForm.value);

    this.isSubmitted = true;
    if (this.loginForm.invalid) {
      console.log("yes")
      return;
    }
    this.authenticationService.userLogin(this.loginForm.get('email').value, this.loginForm.get('password').value)
      .subscribe(data => {
        // console.log("hi",data);
        // localStorage.setItem('user', JSON.stringify(data));
        if (data['role_name'] === 'admin') {
          this.alertService.alertMessage('Login Successfully', 'success', 'check');
          // this.router.navigate(['reports']);
          let str1;
          str1 = window.location.href.split("/")
          let str2 = str1[0] + "//" + str1[2] + '/operator'
          // console.log(str1)
          window.location.href = str2
          // console.log(str2)
        } else if (data['role_name'] === 'operator') {
          this.alertService.alertMessage('Login Successfully', 'success', 'check');
          let str1;
          str1 = window.location.href.split("/")
          let str2 = str1[0] + "//" + str1[2] + '/operator'
          // console.log(str1)
          window.location.href = str2

          // this.router.navigate(['operator']);
        }



        else {
          this.alertService.alertMessage('Unauthorized', 'danger', 'error');
          localStorage.removeItem('livis_user');
        }

        // console.log(data)
      });

    // console.log(this.loginForm.value);
    // this.router.navigateByUrl('/admin');
    // event.preventDefault();
    // console.log(this.loginForm.get('email').value);
    // console.log(event);
    // return false;
    // if (this.loginForm.valid) {
    //   console.log(this.loginForm.value);
    // } else {
    //   console.log(this.loginForm.value);
    //   this.validateAllFormFields(this.loginForm);
    // }

  }

  tabChange(user: string): void {
    this.currentTab = user;

    if (user === 'admin') {
      this.loginForm.controls.workstation_name.clearValidators();
      this.loginForm.controls.workstation_name.updateValueAndValidity();
    } else {
      this.loginForm.controls.workstation_name.setValidators([Validators.required]);
      this.loginForm.controls.workstation_name.updateValueAndValidity();
    }
  }

  getLogoImages(): void {
    this.authenticationService.getLogoImages().subscribe(response => {
      this.logo = response.login_img;
    });
  }

}
