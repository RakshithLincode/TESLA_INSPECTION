


import { Routes, RouterModule } from '@angular/router';
import { AboutUsPageComponent } from './about-us-page/about-us-page.component';



export const AboutUsRoutes: Routes = [
  {
    path: '',
    children: [{
      path: '',
      // component: OperatorPageComponent
      component: AboutUsPageComponent
    }]
  },
]
