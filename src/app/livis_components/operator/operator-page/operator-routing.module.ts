import { Routes, RouterModule } from '@angular/router';
import { OperatorNewComponent } from './operator-new/operator-new.component';
import {OperatorPageComponent} from './operator-page.component';



export const OperatorRoutes: Routes = [
  {
    path: '',
    children: [ {
      path: '',
      // component: OperatorPageComponent
      component: OperatorNewComponent
  }]},
]
