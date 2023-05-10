import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OperatorPanelComponent } from './operator-panel/operator-panel.component';

const routes: Routes = [
  {
    path: '',
    component: OperatorPanelComponent
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OperatorRoutingModule { }
