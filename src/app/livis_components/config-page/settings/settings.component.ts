import { Component, OnInit, ViewChild,ViewEncapsulation } from '@angular/core';
import swal from 'sweetalert2';
import {FormBuilder, FormGroup, Validators,FormArray } from '@angular/forms';
import {AlertService} from '../../../services/alert.service';
import {CdkDragDrop, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';

declare const $: any;

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class SettingsComponent implements OnInit {

  constructor(private _fb: FormBuilder,
    private alertService:AlertService) { }
  settingForm: FormGroup;
  isSubmitted = false;
  available_modules:any;
  enable_modules:any;

  ngOnInit(): void {
    this.loadSettingForm();
    this.available_modules = ["dashboard","operator_management","user_management","config_management"];
    this.enable_modules = [];
  }

  loadSettingForm()
  {
    this.settingForm = this._fb.group({
      client_db_name: ['', [Validators.required]],
      static_path: ['', [Validators.required, ]],
      config_datas: this._fb.array([
        // this.initCamera(),
      ])
    });
    var data:any = [];
    let configs = data.configs;
    if(configs){
      for(let i=0;i<configs.length;i++){
        const control = <FormArray>this.settingForm.controls['config_datas'];
        control.push(this.initCamera(configs[i]));
      }
    }
  }

  initCamera(data:any=[]) {
    return this._fb.group({
        key_config: [data.key1, [Validators.required]],
        value_config: [data.value1,[Validators.required]]
    });
  }

  addConfigData() {
    const control = <FormArray>this.settingForm.controls['config_datas'];
    control.push(this.initCamera());
}

removeConfigData(i: number) {
  const control = <FormArray>this.settingForm.controls['config_datas'];
  control.removeAt(i);
}

drop(event: CdkDragDrop<string[]>) {
  // console.log(this.availables); console.log(this.features); console.log(this.defects);
  if (event.previousContainer === event.container) {
    moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
  } else {
    transferArrayItem(event.previousContainer.data,
                      event.container.data,
                      event.previousIndex,
                      event.currentIndex);
  }
}

updateSettingForm(model)
{
  console.log(model.value);
}
// changePath(fileInput:any)
// {
//   var path = (window.URL || window.webkitURL).createObjectURL(fileInput.target.files[0]);
//   console.log(path);
//   // if (fileInput.target.files && fileInput.target.files[0]) {
//   //   alert("hi");
//   // }else{
//   //   alert("no");
//   // }
//   // console.log(ref);
// }

}
