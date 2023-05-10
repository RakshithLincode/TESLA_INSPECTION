import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../app.module';


import { ShiftComponent } from './shift/shift.component';
import {ConfigsRoutes} from './config-page-routing.module';
import { WorkstationComponent } from './workstation/workstation.component';
import { PartsComponent } from './parts/parts.component';
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';
import { EmailComponent } from './email/email.component';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { SettingsComponent } from './settings/settings.component';
import { MasterFileComponent } from './master-file/master-file.component';




@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(ConfigsRoutes),
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    NgxMaterialTimepickerModule,
    DragDropModule
  ],
  declarations: [
    ShiftComponent,
    WorkstationComponent,
    PartsComponent,
    EmailComponent,
    SettingsComponent,
    MasterFileComponent,

    
  ]
})
export class ConfigPageModule { }
