import { Routes } from '@angular/router';

import { ManageUsersComponent } from './manage-users/manage-users.component';



export const UsersRoutingModule: Routes = [
  {
    path: '',
    children: [
      {
        path: 'users',
        component: ManageUsersComponent,
      },
    ]
  },
  // {
  // path: '',
  // children: [ {
  //   path: 'grid',
  //   component: GridSystemComponent
  // }]
  // }
];
