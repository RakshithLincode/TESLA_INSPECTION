import { Component, OnInit } from '@angular/core';
import PerfectScrollbar from 'perfect-scrollbar';
import { environment } from 'src/environments/environment';
// import from "../../"
let img_base_url = "../../assets/img/";

declare const $: any;

//Metadata
export interface RouteInfo {
  submodules: string[];
  path: string;
  title: string;
  type: string;
  icontype: string;
  collapse?: string;
  children?: ChildrenItems[];
}

export interface ChildrenItems {
  path: string;
  title: string;
  ab: string;
  type?: string;
}


// console.log(user_info);

//Menu Items
let operator_menu = null
let reports_menu = null

let user_info = JSON.parse(localStorage.getItem('livis_user'));

operator_menu={
    path: '/operator',
    title: 'Monitor',
    type: 'link',
    icontype:img_base_url+'monitor.png'
}
reports_menu={
    path: '/report/reports',
    title: 'Statistics',
    type: 'link',
    icontype:img_base_url+'statistics.png'
}
  

export const ROUTES: RouteInfo[] = [
  operator_menu,
  reports_menu
];
@Component({
  selector: 'app-sidebar-cmp',
  templateUrl: 'sidebar-new.component.html',
  styleUrls: ['./sidebar-new.component.css']
})

export class SidebarNewComponent implements OnInit {
  
  languages = [
    { value: 'en', viewValue: '(EN) English' },
    { value: 'de', viewValue: '(DE) German' },
    { value: 'ja', viewValue: '(JA) Japanese' }
  ]
  selectedLanguage = localStorage.getItem('locale') || 'en';
  logoImage: string;
//   livisAppsURL = environment.livis_apps_url;

  public menuItems: any[];
  ps: any;
  userName: any = "";
  isMobileMenu() {
    if ($(window).width() > 991) {

      return false;
    }
    return true;
  };

  constructor() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
    console.log("check", this.menuItems)
  }

  ngOnInit() {
    this.getCurrentLanguage();
    if (window.matchMedia(`(min-width: 960px)`).matches && !this.isMac()) {
      const elemSidebar = <HTMLElement>document.querySelector('.sidebar .sidebar-wrapper');
      this.ps = new PerfectScrollbar(elemSidebar);
    }
    var logoInfo = JSON.parse(localStorage.getItem('user'));
    // this.logoImage = logoInfo.side_nav;
    const user_info = JSON.parse(localStorage.getItem('livis_user'));
    this.userName = user_info ? user_info.first_name : "Sadakat";
  }
  updatePS(): void {
    if (window.matchMedia(`(min-width: 960px)`).matches && !this.isMac()) {
      this.ps.update();
    }
  }
  isMac(): boolean {
    let bool = false;
    if (navigator.platform.toUpperCase().indexOf('MAC') >= 0 || navigator.platform.toUpperCase().indexOf('IPAD') >= 0) {
      bool = true;
    }
    return bool;
  }
  getCurrentLanguage(): void {
    this.selectedLanguage = localStorage.getItem('livisLocale') || 'en';
  }
  setCookie(name, value, days) {
    let expires = '';
    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (value || '') + expires + '; path=/';
  }
  changeLanguage(language: string): void {
    localStorage.setItem('livisLocale', language);
    const locale = { livis_locale: language };
    this.setCookie('livisLocale', JSON.stringify(locale), 365);
    location.reload();
  }
}
