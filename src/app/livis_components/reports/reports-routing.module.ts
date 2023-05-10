import { Routes } from '@angular/router';

import { DefectTypesComponent } from './defect-types/defect-types.component';
import { ProductionQualityComponent } from './production-quality/production-quality.component';
import { ShiftSummaryComponent } from './shift-summary/shift-summary.component';
import { DefectDetailsComponent } from './defect-details/defect-details.component';
import { ReportsNewComponent } from './reports-new/reports-new.component';








export const ReportsRoutes: Routes = [
    {
      path: '',
      children: [ {
        path: 'defectTypes',
        component: DefectTypesComponent
    }]}, 

    {
      path: '',
      children: [ {
        path: 'productionQuality',
        component: ProductionQualityComponent
    }]}, 

    {
      path: '',
      children: [ {
        path: 'shiftSummary',
        component: ShiftSummaryComponent
    }]}, 
    {
      path: '',
      children: [ {
        path: 'defectdetail',
        component: DefectDetailsComponent
    }]}, 
    {
      path: '',
      children: [ {
        path: 'reports',
        component: ReportsNewComponent
    }]}, 
   
  
];
