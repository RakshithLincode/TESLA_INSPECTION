import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AboutUsRoutes } from './about-us-routing.module';
import { AboutUsPageComponent } from './about-us-page/about-us-page.component';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MaterialModule } from 'src/app/app.module';


@NgModule({
  declarations: [AboutUsPageComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(AboutUsRoutes),
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    HttpClientModule
  ]
})
export class AboutUsModule { }
