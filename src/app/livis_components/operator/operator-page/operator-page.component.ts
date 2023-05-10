import { Component, OnInit,ViewEncapsulation} from '@angular/core';
import {MatCheckboxModule} from "@angular/material/checkbox";
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import swal from 'sweetalert2';
import {ShiftService} from "../../../services/shift.service";
import {OperatorService} from '../../../services/operator.service';
import {PmodelService} from "../../../services/pmodel.service";
import {AlertService} from '../../../services/alert.service';
import { AuthenticationService } from '../../../services/authentication.service';
import { StorageService } from '../../../helpers/storage.service';
import { from } from 'rxjs';
import {livisConfig} from "../../../../config/constants";

const demo_config = livisConfig['demo_config'];


declare const $: any;
@Component({
  selector: 'app-operator-page',
  templateUrl: './operator-page.component.html',
  styleUrls: ['./operator-page.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class OperatorPageComponent implements OnInit {
  shift_list:any;
  model_list:any;
  model_info:any;
  metrix_list:any ={};
  defect_list:any[] = null;
  current_process:any = {};
  bath_number_count = 4;
  // camera_urls = 4;
  checkBoxChecked = false;

  callback_seconds = 2000;

  process_id:any = "";
  // process_id:any = "";

  previous_process:any = {}

  process_summary:any = {}
  
  current_inception_id:any = null;
  result_status = null;
  camera_list: [];
  cameraUrlInterval: any;

  constructor(private _fb: FormBuilder,
    private operatorService:OperatorService,
    private shiftService:ShiftService,
    private pmodelService:PmodelService,
    private authenticationService:AuthenticationService,
    private alertService:AlertService,
    private storageService:StorageService
    ) 
    { }
  startProcessForm:FormGroup;
  endProcessForm:FormGroup;
  loginForm:FormGroup;
  updatePartForm:FormGroup;
  isSubmitted = false;
  isSubmittedEdit = false;
  user_unfo:any;
  camera_urls = ["http://127.0.0.1:8000/livis/v1/stream/Maruti_Suzuki/","http://127.0.0.1:8000/livis/v1/stream/Maruti_Suzuki/"];
  defectListInterval:any;
  metrixListInterval:any;
  previousProcessChecked = false;

  cameraLayoutLoad()
  {
    var html = ``;
    
    var count_div = demo_config.CAMERA_SECTION;
    var col_size = demo_config.CAMERA_PARTITION;
    this.camera_list = demo_config.IMAGE_URL;

    // this.getCameraUrl();

    for(var i =0;i<count_div;i++)
    {
      if((this.camera_list[i])){
        html += `<div style="padding-right:5px;padding-left:5px;" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:100%" src="${this.camera_list[i]}" id="live_feed_${(i+1)}" alt="feed not available" >
          </div>`;
      }else{
        html += `<div style="padding-right:5px;padding-left:5px; height:${count_div<=2?'82vh':'41vh'}" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:100%" src="../../../../assets/img/no-camera-live.png" id="live_feed_${(i+1)}" alt="feed not available" >
          </div>`;
      }
    }
    $("#camera_layout_wrap").html(html);
  }

  // getCameraUrl() {
  //   this.operatorService.getCameraUrl().subscribe(data=> {
  //     this.camera_list=data;
  //     this.cameraLayoutLoad();
  //   });
  //   this.cameraUrlInterval = setTimeout(()=> {
  //     this.getCameraUrl();
  //   }, this.callback_seconds);
  // }
  ngOnDestroy()
  {
    if(this.defectListInterval){
      clearTimeout(this.defectListInterval);
    }
    if(this.cameraUrlInterval){
      clearTimeout(this.cameraUrlInterval);
    }
    if(this.metrixListInterval){
      clearTimeout(this.metrixListInterval);
    }
  }
  ngOnInit(): void {
    this.user_unfo = this.storageService.getUserDetails();
    // this.loadStartForm();
    // this.loadEndForm();
    // this.loadLoginForm();
    // this.loadPartForm();
    // this.checkCurrentProcess();
    this.cameraLayoutLoad();
    this.callback_seconds = demo_config.API_CALLBACK_DURATION;
    this.getMetrix();
    // this.shiftService.getShifts()
    //   .subscribe(data =>{
    //     this.shift_list = data;
    // });
    // this.pmodelService.getModels()
    // .subscribe(data =>{
    //  this.model_list = data;
    // });
    // this.alertDefects();  
  }
 
  alertDefects()
  {
    $("#result-status-wrap").removeClass('card-header-success');
    $("#result-status-wrap").addClass('card-header-danger');
    $("#result-status").text("(REJECTED)");
    swal({
      title: "",
      html: "<h1 class='text-danger'>REJECTED</h1>",
      buttonsStyling: false,
      confirmButtonClass: "btn btn-danger",
      type: "error"
  }).catch(swal.noop);
    // swal({
    //   title: "",
    //   html: "<h1 class='text-danger'>REJECTED</h1>",
    //   timer: 2000,
    //   // customClass: 'defect-auto-alert-wrap',
    //   type: 'error',
    //   // width: '90vh',
    
    //   showConfirmButton: false
    // }).catch(swal.noop);
  }

  alertAccepted()
  {
    $("#result-status-wrap").removeClass('card-header-danger');
    $("#result-status-wrap").addClass('card-header-success');
    $("#result-status").text("(ACCEPTED)");

  //   swal({
  //     title: "",
  //     html: "<h1 class='text-success'>ACCEPTED</h1>",
  //     buttonsStyling: false,
  //     confirmButtonClass: "btn btn-success",
  //     type: "success"
  // }).catch(swal.noop);
    swal({
      title: "",
      html: "<h1 class='text-success'>ACCEPTED</h1>",
      timer: 2000,
      // customClass: 'defect-auto-alert-wrap',
      type: 'success',
      // width: '90vh',
    
      showConfirmButton: false
    }).catch(swal.noop);
  }

 
  getMetrix()
  {
    // this.current_process.inception_id = "5ef48d9da16de63e8a575416"
    this.operatorService.getMetrix(this.current_process.inception_id)
      .subscribe(data =>{
        this.result_status = data.data;
        // this.result_status = null;
        this.defect_list = data.defect_list;
        let set_list = new Set(this.defect_list);
        this.defect_list=Array.from(set_list);

        console.log(this.defect_list);

        if(this.defect_list.length==0) {
          this.defect_list = null;
          console.log("EMPTY");
        }

        // console.log("RESULT STATUS",this.result_status);
    }, error=> {
      console.log("ERROR:",error);
    });
    this.metrixListInterval = setTimeout(()=> {
      this.getMetrix();
    }, this.callback_seconds);
  }

  

  

 

 
  



}
