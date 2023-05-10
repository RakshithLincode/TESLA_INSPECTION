import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MdModule } from '../../md/md.module';
import { MaterialModule } from '../../app.module';

import { OperatorRoutingModule } from './operator-routing.module';
import { OperatorPanelComponent } from './operator-panel/operator-panel.component';


@NgModule({
  declarations: [OperatorPanelComponent],
  imports: [
    CommonModule,
    OperatorRoutingModule,
    FormsModule,
    MdModule,
    MaterialModule
  ]
})
export class OperatorModule { }
