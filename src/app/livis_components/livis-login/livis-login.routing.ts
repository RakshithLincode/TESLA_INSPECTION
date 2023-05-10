import { Routes } from '@angular/router';

import { LivisLoginComponent } from './livis-login.component';

export const LivisLoginRoutes: Routes = [
    {

      path: '',
      children: [ {
        path: 'login',
        component: LivisLoginComponent
    }]
}
];