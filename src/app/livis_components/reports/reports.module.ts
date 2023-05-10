import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../app.module';
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';

import { DefectTypesComponent } from './defect-types/defect-types.component';
import {ReportsRoutes} from './reports-routing.module';
import { ProductionQualityComponent } from './production-quality/production-quality.component';
import { ShiftSummaryComponent } from './shift-summary/shift-summary.component';
import { DefectDetailsComponent } from './defect-details/defect-details.component';
import { ReportsNewComponent } from './reports-new/reports-new.component';



// import {NgbDate} from '@ng-bootstrap/ng-bootstrap';
// import { NgbModule } from '@ng-bootstrap/ng-bootstrap';




@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(ReportsRoutes),
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    NgxMaterialTimepickerModule,
    NgxDaterangepickerMd
    // NgbDate
  ],
  declarations: [
    DefectTypesComponent,
    ProductionQualityComponent,
    ShiftSummaryComponent,
    DefectDetailsComponent,
    ReportsNewComponent
    
  ]
})
export class ReportsPageModule { }
