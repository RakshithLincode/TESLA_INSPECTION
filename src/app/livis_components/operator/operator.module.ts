import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../app.module';


import { OperatorPageComponent } from './operator-page/operator-page.component';
import {OperatorRoutes} from './operator-page/operator-routing.module';
import { OperatorNewComponent } from './operator-page/operator-new/operator-new.component';


import { HttpClientModule } from '@angular/common/http';



@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(OperatorRoutes),
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  declarations: [
    // OperatorPageComponent,
    OperatorNewComponent
  ]
})
export class OperatorModule { }
