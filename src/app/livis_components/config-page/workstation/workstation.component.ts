import { Component, OnInit, ViewChild,ViewEncapsulation } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import swal from 'sweetalert2';
import {WorkstationService} from "../../../services/workstation.service";
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ArrayType } from '@angular/compiler';
import {AlertService} from '../../../services/alert.service'


declare const $: any;
@Component({
  selector: 'app-workstation',
  templateUrl: './workstation.component.html',
  styleUrls: ['./workstation.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class WorkstationComponent implements OnInit {
  // workstationForm;
  workstationForm: FormGroup; // our form model
  workstationFormEdit:FormGroup;
  // @Input() inputArray: ArrayType[];
  isSubmitted = false;
  isSubmitedEdit = false;

  displayedColumns = ['workstation_name','ip','port','status','camera','operation'];
  dataSource: MatTableDataSource<any>;
  dataLength: number;
  cameraDetailsHeading = ['SN','Camera Id','Camera Name'];
  cameraInfo:any;
  // statusActive = '<span class="material-icons">fiber_manual_record </span>';
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  constructor(private workstationService:WorkstationService,
    private _fb: FormBuilder,
    private alertService:AlertService
    ) 
  { }

  ngOnInit() {
    this.loadAddForm();
    this.loadEditForm(); 
    this.getWorkStationList();
  }


  ngAfterViewInit() {

    // this.dataSource.paginator = this.paginator;
    // this.dataSource.sort = this.sort;
    // console.log(this.dataSource);
  }

  loadAddForm()
  {
    this.workstationForm = this._fb.group({
      workstation_name: ['', [Validators.required, Validators.minLength(3)]],
      workstation_ip: ['', [Validators.required, ]],
      workstation_port: ['', [Validators.required,]],
      workstation_status: ['', ],
      cameras: this._fb.array([
          this.initCamera(),
      ])
  });


  }

loadEditForm(data:any = [])
{
  this.workstationFormEdit = this._fb.group({
    _id: [data._id, ],
    edit_workstation_name: [data.workstation_name, [Validators.required, Validators.minLength(3)]],
    edit_workstation_ip: [data.workstation_ip, [Validators.required, ]],
    edit_workstation_port: [data.workstation_port, [Validators.required,]],
    edit_workstation_status: [data.workstation_status, [Validators.required, ]],
    camerasEdit: this._fb.array([
        // this.initCameraEdit(),
    ])
  });
  let camera_info = data.cameras;
  if(camera_info){
    for(let i=0;i<camera_info.length;i++){
      const control = <FormArray>this.workstationFormEdit.controls['camerasEdit'];
      control.push(this.initCameraEdit(camera_info[i]));
    }
  }

}

editWorkStation(id)
{
  // alert(id);
  // let edit_data = {
  //   "workstation_name": "djdjd",
  //   "workstation_ip": "14566",
  //   "workstation_port": "7000",
  //   "workstation_status": true,
  //   "cameras": [{
  //     "camera_id": "ddbhsjh",
  //     "camera_name": ""
  //   }, {
  //     "camera_id": "ss",
  //     "camera_name": "sss"
  //   }]
  // }
  this.workstationService.getWorkStation(id)
    .subscribe(data =>{
      this.loadEditForm(data);
      $("#edit-workstation-modal").modal("show");
    });
 

  // $('.modal').modal('hide');

  
}



initCamera() {
    return this._fb.group({
        camera_id: ['', Validators.required],
        camera_name: ['']
    });
}

initCameraEdit(data:any=[]) {
  return this._fb.group({
      edit_camera_id: [data.camera_id, Validators.required],
      edit_camera_name: [data.camera_name]
  });
}

getWorkStationList()
{
  this.workstationService.getWorkStations()
    .subscribe(data =>{
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.data = data;
      this.dataLength = data.length;

      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
}

  
  filterWorkStation(value: string):void{
    this.dataSource.filter = value.trim().toLowerCase();
  }

  addWorkstation()
  {
    // console.log(this);
    $("#add-workstation-modal").modal("show");

  }



addCamera() {
    const control = <FormArray>this.workstationForm.controls['cameras'];
    control.push(this.initCamera());
}

addCameraEdit() {
  const control = <FormArray>this.workstationFormEdit.controls['camerasEdit'];
  control.push(this.initCameraEdit());
}

removeCamera(i: number) {
    const control = <FormArray>this.workstationForm.controls['cameras'];
    control.removeAt(i);
}

removeCameraEdit(i: number) {
  const control = <FormArray>this.workstationFormEdit.controls['camerasEdit'];
  control.removeAt(i);
}

addNewWorkStation(model) {
  this.isSubmitted = true;
  if(!this.workstationForm.invalid){
  
    this.workstationService.addWorkStation(model.value)
          .subscribe(data =>{
            this.alertService.alertMessage("Added Successfully","success","check");
    });
    this.isSubmitted = false;
    // model.resetForm();
    // this.workstationForm.reset();
    this.getWorkStationList();
    this.loadAddForm();
    
    $("#add-workstation-modal").modal("hide");
  }
}


getCameraDetails(id)
{
  // this.cameraInfo = 
  //    [{
  //     "camera_id": "ddbhsjh",
  //     "camera_name": ""
  //   }, {
  //     "camera_id": "ss",
  //     "camera_name": "sss"
  //   }]

    this.workstationService.getWorkStation(id)
    .subscribe(data =>{
      this.cameraInfo = data.cameras;
      $("#camera-details-modal").modal("show");
    });
 
}

updateWorkStation(model)
{
  this.isSubmitedEdit = true;
  if(!this.workstationFormEdit.invalid){
  
    this.workstationService.updateWorkStation(model.value)
          .subscribe(data =>{
            this.alertService.alertMessage("Updated Successfully","success","check");
            this.isSubmitedEdit = false;
            this.getWorkStationList();
            $("#edit-workstation-modal").modal("hide");
           
    });
    

  }
}


deleteWorkstation(id)
{
  swal({
    title: 'Are you sure?',
    text: 'You will not be able to recover this workstation!',
    type: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'No, keep it',
    confirmButtonClass: "btn btn-success",
    cancelButtonClass: "btn btn-danger",
    buttonsStyling: false
}).then((result) => {
  if (result.value) {
    this.workstationService.deleteWorkStation(id)
    .subscribe(data =>{
      this.getWorkStationList();
      swal({
        title: 'Deleted!',
        text: 'Your workstation info has been deleted.',
        type: 'success',
        confirmButtonClass: "btn btn-success",
        buttonsStyling: false
    }).catch(swal.noop)
    });
    
  } else {
    swal({
        title: 'Cancelled',
        text: 'Your workstation info is safe :)',
        type: 'error',
        confirmButtonClass: "btn btn-info",
        buttonsStyling: false
    }).catch(swal.noop)
  }
})
}








}
