import { Routes } from '@angular/router';

import { AdminLayoutComponent } from './layouts/admin/admin-layout.component';
import { AuthLayoutComponent } from './layouts/auth/auth-layout.component';
import { LivisLogoutComponent } from './livis_components/livis-logout/livis-logout.component';
import { AdminGuard } from './helpers/admin.guard';
import { AuthGuard } from './helpers/auth.guard';
// import { LivisLogoutComponent } from './livis_components/livis-logout/livis-logout.component';


import { NoContentComponent } from './livis_components/no-content/no-content.component';
import { AccessDeniedComponent } from './livis_components/access-denied/access-denied.component';
import { LivisProfileComponent } from './livis_components/livis-profile/livis-profile.component';
import { OperatorGuard } from './helpers/operator.guard';
// import { QrcodePrintComponent } from './livis_components/operator/qrcode-print/qrcode-print.component';

// import { AppsComponent } from './livis_components/apps/apps.component';

export const AppRoutes: Routes = [
  {
    path: '',
    redirectTo: 'auth/login',
    pathMatch: 'full',
  },
  {
    path: '',
    component: AdminLayoutComponent,
    // canActivate: [AdminGuard],
    children: [
      // {
      //     path: '',
      //     loadChildren: './dashboard/dashboard.module#DashboardModule',
      //     // canActivate: [AdminGuard],
      // },
      // {
      //   path: 'dashboard',
      //   loadChildren: './livis_components/livis-dashboard/livis-dashboard.module#LivisDashboardModule',
      //   // canActivate: [AdminGuard]
      // },
      {
        path: 'config',
        loadChildren: './livis_components/config-page/config-page.module#ConfigPageModule',
        canActivate: [AuthGuard, AdminGuard]

      },

      {
        path: 'user',
        loadChildren: './livis_components/users/users.module#UsersModule',
        canActivate: [AuthGuard, AdminGuard]
        // canActivate: [AdminGuard],
      },
      {
        path: 'aboutus',
        loadChildren: './livis_components/about-us/about-us.module#AboutUsModule',
        // canActivate: [AdminGuard],
      },
      {
        path: 'operator',
        loadChildren: './livis_components/operator/operator.module#OperatorModule',
        canActivate: [AuthGuard, OperatorGuard]
      },
      // {
      //   path: 'report',
      //   loadChildren: './livis_components/summary-reports/summary-reports.module#SummaryReportsModule',
      //   canActivate: [AuthGuard]
      // },
      {
        path: 'myprofile',
        component: LivisProfileComponent,
        canActivate: [AuthGuard]
      },
      {
        path: 'report',
        loadChildren: './livis_components/reports/reports.module#ReportsPageModule',
        canActivate: [AuthGuard]
      },
    ]
  },

  {
    path: '',
    component: AuthLayoutComponent,
    children: [{
      path: 'auth',
      loadChildren: './livis_components/livis-login/livis-login.module#LivisLoginModule'
    }]
  },

  {
    path: 'logout',
    component: LivisLogoutComponent,
  },
  // { path: 'operator/print',
  // // outlet: 'QrcodePrintComponent',
  // component: QrcodePrintComponent,

  // },
  // {
  //   path: 'livis/apps',
  //   component: AppsComponent,
  //   canActivate: [AuthGuard]
  // },

  // {
  //     path: 'logout',
  //     component: LivisLogoutComponent,
  // }
  // ,
  // {
  //     path: 'access-denied',
  //     component: AccessDeniedComponent
  // },
  {
    path: '**',
    component: NoContentComponent
  },





];
