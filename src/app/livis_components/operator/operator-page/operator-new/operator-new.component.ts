import { StorageService } from '../../../../helpers/storage.service';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import swal from 'sweetalert2';
import { ShiftService } from '../../../../services/shift.service';
import { AlertService } from '../../../../services/alert.service';
import { AuthenticationService } from '../../../../services/authentication.service';
// import { PlanningService } from 'src/app/services/planning.service';
import { PmodelService } from 'src/app/services/pmodel.service';
import { OperatorService } from 'src/app/services/operator.service';
import { ChangeDetectorRef } from '@angular/core';
import { MarutiOperatorService } from 'src/app/services/maruti-operator.service';
import { livisConfig } from "../../../../../config/constants";
import { identifierModuleUrl } from '@angular/compiler';

const demo_config = livisConfig['demo_config'];

// import {ToyodaPartService} from "../../../services/toyoda-part.service";

declare const $: any;
@Component({
  selector: 'app-operator-new',
  templateUrl: './operator-new.component.html',
  styleUrls: ['./operator-new.component.css'],
  encapsulation: ViewEncapsulation.Emulated
})
export class OperatorNewComponent implements OnInit {
  user_info: any;
  camera_urls: any = [];
  loginForm: FormGroup;
  inspectionQcForm: FormGroup;
  pdnCounterForm: FormGroup;
  processStartForm: FormGroup;
  setConfiguration: FormGroup;
  rescanForm: FormGroup;
  isSubmitted = false;
  part_list = [];
  current_process: any = {};
  metrix_list: any = {};

  defect_list: any = [];
  current_inspection_id: any = null;
  defectListInterval: any;
  metrixListInterval: any;
  runningProcessInterval: any;

  border = [];
  process_summary: any = {};
  production_counter: any;
  inspection_count = 0;
  cancel_text: any = 'Cancel';
  planInfo: any;
  shiftInfo: any;
  partInfo: any;
  isEditing = false;

  sealentMin: number;
  editSealentMin = false;
  sealentMax: number;
  editSealentMax = false;
  flangeMin: number;
  editFlangeMin = false;
  flangeMax: number;
  editFlangeMax = false;
  breakageMin: number;
  editBreakageMin = false;
  breakageMax: number;
  editBreakageMax = false;
  masticSealentMin: number;
  editMasticSealentMin = false;
  masticSealentMax: number;
  editMasticSealentMax = false;

  dimensions = {
    sealentMin: 0,
    sealentMax: 0,
    flangeMin: 0,
    flangeMax: 0,
    breakageMin: 0,
    breakageMax: 0,
    masticSealentMin: 0,
    masticSealentMax: 0,
  };

  reached_status_alert = false;
  selected_part_item: any = "";
  isProcessRunning: boolean = false;
  ocr_status: any;
  burr_status: any;
  running_inspection_id: any = null;
  selectedPartName: any;
  total_count: any = null;
  total_accepted: any = null;
  total_rejected: any = null;
  border_ocr: any = [];
  overall_status: any;
  inspection_status: any = '--';
  reasons: any;
  border_defect: [];
  dent_on_elastomer: any;
  dent_on_thermostat: any;
  saw_tooth_damage: any;
  thread_damage: any;
  printing_erase: any;
  nextSlideLength: any = 0;
  pageNumber: any = parseInt(localStorage.getItem('carousal-page-number')) / 8 + 1;
  thermostat_printing_erase: any;
  elastomer_printing_erase: any;
  camera_list: any = [];
  acceptedCount: any;
  totalCount: any;
  rejectedCount: any;
  inspection_payload: any;
  partafterSelect: any;
  isSubmittedConfig: boolean = false;
  rows: any;
  columns: any;
  thresholdForm: FormGroup;
  threshold: any;
  Apicalldone: boolean = false;
  inferenceFrame: any;
  inspectShow: boolean = true;
  showEditIcon: boolean = false;
  buttonText: string = "Inspect";
  threshold_actual: any;
  defects: any;
  label_to_sealent_measurment: any;
  label_angle: any;
  centroid_to_edge_value_1: any;
  centroid_to_edge_value_2: any;
  radius_defect_value: any;
  left_radius: any;
  left_length: any;
  right_radius: any;
  right_length: any;


  constructor(
    private _fb: FormBuilder,
    private operatorService: OperatorService,
    private shiftService: ShiftService,
    // private planService: PlanningService,
    private partService: PmodelService,
    private authenticationService: AuthenticationService,
    private alertService: AlertService,
    private storageService: StorageService,
    private marutiService: OperatorService,
    private cdref: ChangeDetectorRef,

  ) { }

  ngOnInit(): void {
    this.user_info = this.storageService.getUserDetails();
    this.loadProcessStartForm()
    this.loadthresholdForm()
    this.loadsetConfigurationForm()
    this.getPartList();

    this.getRunningProcess()
    // this.cameraLayoutLoad();
    // this.getCameraFeedUrl()
    // for(let i=0;i<2;i++) {
    //   document.getElementById(`full-screen-icon-open-${i}`).addEventListener('click',this.goFullScreen.bind(this))
    // }
  }


  loadProcessStartForm() {
    this.processStartForm = this._fb.group({
      // workstation_id: ['', [Validators.required]],
      // operator_id: ['', [Validators.required]],
      part_name: ['', [Validators.required]],
      // part_id: ['', [Validators.required]],
    });
  }
  loadthresholdForm() {
    this.thresholdForm = this._fb.group({
      top: ['', [Validators.required]],
      bottom: ['', [Validators.required]],
      left: ['', [Validators.required]],
      // right: ['', [Validators.required]],
    });
  }

  getPartList() {
    ////////console.log("INSIDE GET ALL PARTS")
    this.marutiService.getAllParts().subscribe((data) => {
      this.part_list = data;
      ////////console.log("GET ALL PARTS==============================>", this.part_list);

    });
  }

  getCameraFeedUrl() {
    console.log("INSIDE GCFU");
    this.operatorService
      .getCameraFeed()
      .subscribe((data) => {
        this.camera_urls = data.data;
        ////////console.log(this.camera_urls)
        // this.cameraLayoutLoad();
        this.cameraLayoutLoad();

      });
  }


  // function for mulitple camera feed with mulitple accept reject control 
  // cameraLayoutLoad() {
  //   var html = ``;

  //   var count_div = 4;
  //   var col_size = 6;
  //   this.camera_list = [];
  //   var camera_list = [];


  //   for (var i = 0; i < count_div; i++) {
  //     if (camera_list[i]) {
  //       html += `<div style="position:relative !important;padding-right:5px;padding-left:5px; height:${count_div <= 2 ? '85vh' : '40vh'
  //         }" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
  //       <div  class="fullscreen-box" style="position:absolute !important; top: 15px; right:15px;  z-index: 100 !important;" (click)="goFullScreen()" id="full-screen-icon-open-${i}">
  //         <span><img src="../../../../../assets/img/fullscreen.png" width= "25px" alt=""></span>
  //       </div>

  //       <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important;">
  //               <span><img src="../../../../../assets/img/live.png"     width= "100%" alt=""></span>
  //       </div>
  //       <div  class="status-box" style="    position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important;">
  //             <div class="status-status-box" id="status-box-${i}" style="display: flex;justify-content: center; align-items: center;background-color: var(--livis-bg-color);color: var(--livis-color);box-shadow: 0 2px 2px 0 rgb(55 197 171 / 14%), 0 3px 1px -2px rgb(55 197 171 / 20%), 0 1px 5px 0 rgb(55 197 171 / 12%);border-radius: 12px;max-width: 100px !important;">`;
  //       if (this.inspection_status != '--') {

  //         for (let j = 0; j < this.inspection_status[i].length; j++) {
  //           if (this.inspection_status[i] == "Rejected") {
  //             html += `<span   style="background: red !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Rejected</span>`
  //           } else {
  //             html += `<span   style="background: green !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Accepted</span>`
  //           }
  //         }
  //       }
  //       `

  //             </div>
  //             <div  class="defect-under-status row" style="margin-top: 10px !important;background: none !important;color: white !important;">`;
  //       if (this.defect_list && this.defect_list.length > 0) {

  //         for (let j = 0; j < this.defect_list[i].length; j++) {
  //           html += `<span class=" col-md-12 col-md-12 status-defect" style="padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;"> ${this.defect_list[i][j]} </span>`
  //         }
  //       }
  //       html += ` </div> 
  //       </div>


  //       <img style="width:100%;height:100%" src="http://${
  //         // camera_list[i + this.nextSlideLength]
  //         camera_list[i]
  //         }" id="live_feed_${i + 1}" alt="feed not available" >
  //         </div>`;


  //     } else {
  //       html += `<div style="position:relative !important ;padding-right:5px;padding-left:5px; height:${count_div <= 2 ? '85vh' : '43vh'
  //         }" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" id="full-view-${i}" >
  //       <div  class="fullscreen-box" style="position:absolute !important; top: 15px; right:15px;  z-index: 100 !important;" (click)="goFullScreen()" id="full-screen-icon-open-${i}">
  //         <span><img src="../../../../../assets/img/fullscreen.png" width= "25px" alt=""></span>
  //       </div>


  //       <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important;">
  //               <span><img src="../../../../../assets/img/live.png"     width= "100%" alt=""></span>
  //       </div>
  //       <div  class="status-box" style="    position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important;">
  //             <div class="status-status-box" id="status-box-${i}" style="display: flex;justify-content: center; align-items: center;background-color: var(--livis-bg-color);color: var(--livis-color);box-shadow: 0 2px 2px 0 rgb(55 197 171 / 14%), 0 3px 1px -2px rgb(55 197 171 / 20%), 0 1px 5px 0 rgb(55 197 171 / 12%);border-radius: 12px;max-width: 100px !important;">`;
  //       if (this.inspection_status != '--') {

  //         for (let j = 0; j < this.inspection_status[i].length; j++) {
  //           if (this.inspection_status[i] == "Rejected") {
  //             html += `<span   style="background: red !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Rejected</span>`
  //           } else {
  //             html += `<span   style="background: green !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Accepted</span>`
  //           }
  //         }
  //       }
  //       `</div>
  //             <div  class="defect-under-status row" style="margin-top: 10px !important;background: none !important;color: white !important;">`;
  //       if (this.defect_list && this.defect_list.length > 0) {

  //         for (let j = 0; j < this.defect_list[i].length; j++) {
  //           html += `<span class=" col-md-12 col-md-12 status-defect" style="padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;"> ${this.defect_list[i][j]} </span>`
  //         }
  //       }
  //       html += ` </div> 
  //       </div>

  //       <img style="width:100%;height:100%" src="../../../../assets/img/backpreview.png" id="live_feed_${i + 1
  //         }" alt="feed not available" >

  //         </div>`;
  //     }
  //   }
  //   $("#camera_layout_wrap").html(html);
  //   for (let i = 0; i < 4; i++) {
  //     document.getElementById(`full-screen-icon-open-${i}`).addEventListener('click', this.goFullScreen.bind(this))
  //   }
  // }



  // function for multiple images with single status 
  cameraLayoutLoad() {
    var html = ``;

    var count_div = 2;
    var col_size = 6;
    this.camera_list = [];
    var camera_list = this.camera_urls;
    //console.log(this.camera_urls)

    for (var i = 0; i < count_div; i++) {
      if (camera_list[i]) {
        html += `<div style="position:relative !important;padding-right:5px;padding-left:5px; height:${count_div <= 2 ? '85vh' : '42vh'
          }" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" id="full-view-${i}">
          <div  class="fullscreen-box" style="position:absolute !important; top: 15px; right:15px;  z-index: 100 !important;" (click)="goFullScreen()" id="full-screen-icon-open-${i}">
          <i class="material-icons cross-icon" style="color: white !important; font-size : 24px !important; cursor: pointer !important">fullscreen</i>
        </div>
        <div  class="fullscreen-box invisible" style="position:absolute !important; top: 15px; right:40px;  z-index: 100 !important;" (click)="exitFullScreen()" id="full-screen-icon-close-${i}">
        <i class="material-icons cross-icon" style="color: white !important; font-size : 24px !important; cursor: pointer !important">fullscreen_exit</i>
        </div>
        `;
        if (i == 0) {
          html += ` 
          <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                  <span style="color : white; font-size : 12px !important" >Live Feed</span>
          </div>`
        }else if (i == 1) {
            html += ` 
          <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                  <span style="color : white; font-size : 12px !important" >Predicted Image</span>
          </div>`
          } else if (i == 2) {
            html += ` 
          <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                  <span style="color : white; font-size : 12px !important" >Mask Image</span>
          </div>`
        } else if (i == 3) {
          html += ` 
          <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                  <span style="color : white; font-size : 12px !important" >Defect Details Image</span>
          </div>`
        }
        html +=
          `
        <div  class="status-box" style="    position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important;">
              <div class="status-status-box" id="status-box-${i}" style="display: flex;justify-content: center; align-items: center;background-color: var(--livis-bg-color);color: var(--livis-color);box-shadow: 0 2px 2px 0 rgb(55 197 171 / 14%), 0 3px 1px -2px rgb(55 197 171 / 20%), 0 1px 5px 0 rgb(55 197 171 / 12%);border-radius: 12px;max-width: 100px !important;">
              </div>
              <div  class="defect-under-status row" style="margin-top: 10px !important;background: none !important;color: white !important;"></div> 
        </div>
        <img style="width:100%;height:100%; border-radius : 12px" src="${camera_list[i]
          }" id="live_feed_${i + 1}" alt="feed not available" >
          </div>`;
      } else {
        html += `<div style="position:relative !important ;padding-right:5px;padding-left:5px; height:${count_div <= 2 ? '85vh' : '42vh'
          }" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" id="full-view-${i}" >
          <div  class="fullscreen-box" style="position:absolute !important; top: 15px; right:15px;  z-index: 100 !important;" (click)="goFullScreen()" id="full-screen-icon-open-${i}">
            <i class="material-icons cross-icon" style="color: white !important; font-size : 24px !important; cursor: pointer !important">fullscreen</i>
          </div>
          <div  class="fullscreen-box invisible" style="position:absolute !important; top: 15px; right:40px;  z-index: 100 !important;" (click)="exitFullScreen()" id="full-screen-icon-close-${i}">
          <i class="material-icons cross-icon" style="color: white !important; font-size : 24px !important; cursor: pointer !important">fullscreen_exit</i>
          </div>
          `;
        if (i == 0) {
          html += ` 
            <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                    <span style="color : white; font-size : 12px !important" >Live Feed</span>
            </div>`
        } else
          if (i == 1) {
            html += ` 
            <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                    <span style="color : white; font-size : 12px !important" >Predicted Image</span>
            </div>`
          } else if (i == 2) {
            html += ` 
            <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                    <span style="color : white; font-size : 12px !important" >Mask Image</span>
            </div>`
          } else if (i == 3) {
            html += ` 
            <div  class="live-box" style="position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important; background : #1da2bf; padding-inline : 10px; border-radius : 6px">
                    <span style="color : white; font-size : 12px !important" >Defect Details Image</span>
            </div>`
          }
        html +=
          `
          <div  class="status-box" style="    position:absolute !important;bottom: 15px;left:15px;z-index: 100 !important;">
                <div class="status-status-box" id="status-box-${i}" style="display: flex;justify-content: center; align-items: center;background-color: var(--livis-bg-color);color: var(--livis-color);box-shadow: 0 2px 2px 0 rgb(55 197 171 / 14%), 0 3px 1px -2px rgb(55 197 171 / 20%), 0 1px 5px 0 rgb(55 197 171 / 12%);border-radius: 12px;max-width: 100px !important;"></div>
                <div  class="defect-under-status row" style="margin-top: 10px !important;background: none !important;color: white !important;"></div> 
          </div>
  
          <img style="width:100%;height:100%" src="../../../../assets/img/backpreview.png" id="live_feed_${i + 1
          }" alt="feed not available" >
  
            </div>`;
      }
    }
    $("#camera_layout_wrap").html(html);
    for (let i = 0; i < 4; i++) {
      document.getElementById(`full-screen-icon-open-${i}`).addEventListener('click', this.goFullScreen.bind(this))
      document.getElementById(`full-screen-icon-close-${i}`).addEventListener('click', this.exitFullScreen.bind(this))
    }
  }


  // cameraLayoutLoad() {
  //   var html = ``;

  //   var count_div =4;
  //   var col_size = 6;
  //   this.camera_list =[];   
  //    this.camera_list =this.camera_urls;
  //   //  this.camera_list = demo_config.IMAGE_URL;
  //   ////////console.log(this.camera_list)

  //   // this.getCameraUrl();

  //   for (var i = 0; i < count_div; i++) {
  //     if ((this.camera_list[i])) {
  //       html += `<div style="padding:5px !important" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
  //       <img style="width:100%;height:44vh; border-radius:15px !important" src="${this.camera_list[i]}" id="live_feed_${(i + 1)}" alt="feed not available"  >
  //         </div>`;
  //     } else {
  //       html += `<div style="padding:5px !important; height:44vh" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
  //       <img style="width:100%;height:44vh; border-radius:15px !important" src="../../../../../assets/img/backpreview.png" id="live_feed_${(i + 1)}" alt="feed not available" >
  //         </div>`;
  //     }
  //   }
  //   $("#camera_layout_wrap").append(html);
  // }


  getRunningProcess() {
    console.log("GET RUNNING PROCESS" )
    this.marutiService
      .getRunningProcess()
      .subscribe((data: any) => {
        // if (data[0] == null) {
        //   return
        // }
        ////////console.log(data[0]==null)
        this.isProcessRunning = true;
        this.current_process = data;
        this.running_inspection_id = data.inspection_id;
        this.selectedPartName = this.processStartForm.value.part_name;
        this.partafterSelect = data.part_name

        this.getMetrix();
        $('#start_process_btn').addClass('invisible');
        $('#configure_btn').addClass('invisible');
        $('#stop_process_btn').removeClass('invisible');
        $('#inspect_btn').removeClass('invisible');
        $('#inspect_btn_wait').removeClass('invisible');
        this.getCameraFeedUrl();
        this.camera_urls = demo_config.IMAGE_URL;
        // this.cameraLayoutLoad()
        // }

        // }
        // } else {

        // }
      },);


  }


  showStartForm() {
    $('#process-start-modal').modal('show');
  }
  partChange(value) {
    ////////console.log(value)
    this.selected_part_item = value;


    this.processStartForm.patchValue({
      // operator_id: this.user_info.user_id,
      part_name: this.selected_part_item,
    });
    ////////console.log("ON CHANGE",this.selected_part_item);
    this.cdref.detectChanges();
  }

  startProcess(model: any) {

    ////////console.log("MODEL SEL", this.processStartForm);
    // ////////console.log(this.user_info)
    this.isProcessRunning = true;
    if (this.processStartForm.value.part_name == "") {
      return
    }
    let body = {
      // user_id: this.user_info._id,
      part_name: this.processStartForm.value.part_name,
    }
    this.marutiService.startProcess(body).subscribe((data) => {
      ////////console.log("INSIDE STARTING")
      this.alertService.alertMessage(
        'Process Started Successfully',
        'success',
        'check'
      );
      // this.Apicalldone = !this.Apicalldone;
      // $('#inspect_btn').addClass('invisible');
      this.current_process.inspection_id = data.current_inspection_id;
      this.selectedPartName = this.processStartForm.value.part_name;

      this.getRunningProcess();
      // this.getCameraFeedUrl();
        this.inspectShow = true;
      $('#configure_btn').addClass('invisible');
      $('#start_process_btn').addClass('invisible');
      $('#stop_process_btn').removeClass('invisible');
      $('#inspect_btn').removeClass('invisible');
      $('#inspect_btn_wait').removeClass('invisible');

      $('#process-start-modal').modal('hide');
    }, error => {
      ////////console.log("NO SHIFT");
    });

  }

  processEndForm() {
    swal({
      title: '',
      text: 'Are you sure you want to end process',
      type: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Ok',
      cancelButtonText: 'Cancel',
      confirmButtonClass: 'btn btn-success',
      cancelButtonClass: 'btn btn-danger',
      buttonsStyling: false,
    }).then((result) => {
      if (1) {
        if (result.value) {
          const end_info = { inspection_id: this.running_inspection_id };

          this.marutiService.endProcess(end_info).subscribe((response) => {
            $('#stop_process_btn').addClass('invisible');
            $('#inspect_btn').addClass('invisible');
            $('#inspect_btn_wait').addClass('invisible');
            $('#start_process_btn').removeClass('invisible');
            $('#configure_btn').removeClass('invisible');
            $('#result-status-text').text('');
            ////////console.log("INSIDE END!!!!!!!!!!!!!!!!!!!!!!!!!!", this.metrixListInterval);
            if (this.metrixListInterval) {
              clearTimeout(this.metrixListInterval);
            }
            this.inspection_status = "--";
            ////////console.log(this.inspection_status)
            this.defect_list = [""]
            this.acceptedCount = 0
            this.rejectedCount = 0
            this.totalCount = 0
            this.selected_part_item = ""
            this.camera_urls = [""]
            this.cameraLayoutLoad()

          });
        }
      } else {
        this.quantityAlert();
      }
    });
  }


  quantityAlert() {
    swal({
      title: 'Quantity Alert',
      html:
        "<h4 class='text-danger'>Planned production not achieved.You cant end the process</h4>",
      buttonsStyling: false,
      confirmButtonClass: 'btn btn-danger',
      type: 'error',
    }).catch(swal.noop);
  }

  processEndedAlert() {
    this.current_process = {};
    this.partInfo = {};
    this.planInfo = {};
    this.shiftInfo = {};
    this.defect_list = [];
    this.metrix_list = {};

    if (this.runningProcessInterval) {
      clearTimeout(this.runningProcessInterval);
    }
    if (this.defectListInterval) {
      clearTimeout(this.defectListInterval);
    }
    if (this.metrixListInterval) {
      clearTimeout(this.metrixListInterval);
    }
    swal({
      title: '',
      html: "<h3 class='text-success'>Process Ended</h3>",
      buttonsStyling: false,
      confirmButtonClass: 'btn btn-success',
      type: 'success',
    }).catch(swal.noop);
  }


  endmetrix() {
    this.marutiService.getMetrix(this.running_inspection_id).subscribe((data: any) => {
      let result;

      this.inspection_status = data.status;
      ////////console.log(this.inspection_status)
      this.defect_list = data.defect_list
      this.acceptedCount = data.total_accepted
      this.rejectedCount = data.total_rejected
      this.totalCount = data.total
    });
  }


  getMetrix() {
    ////////console.log("getmetrix")
    this.marutiService.getMetrix(this.running_inspection_id).subscribe((data: any) => {
      let result;
      // this.selected_part_item = data.part_name
      // //////console.log(this.selected_part_item)
      // this.inspection_status = data.status;
      // ////////console.log(this.inspection_status)
      // this.defect_list = data.defect_list
      // this.acceptedCount = data.total_accepted
      // this.rejectedCount = data.total_rejected
      // this.totalCount = data.total
      this.selected_part_item = data.part_name
      //////console.log(this.selected_part_item)
        // if (data.total_accepted != this.acceptedCount || data.total_rejected != this.rejectedCount) {
        //   this.Apicalldone =true
        //   this.inspectShow = true
        //   this.getCameraFeedUrl()
        // }
        if (data.total_accepted != this.acceptedCount || data.total_rejected != this.rejectedCount) {
          $('#inspect_btn').removeClass('invisible');
          this.Apicalldone = false
          this.buttonText = "Inspect"
          this.getCameraFeedUrl()
        }
      this.inspection_status = data.status;
      this.inferenceFrame = data.inference_frames
      ////////console.log(this.inspection_status)
      this.label_angle = data.label_angle ? data.label_angle : false
      this.centroid_to_edge_value_1 = data.centroid_to_edge_value_1 ? data.centroid_to_edge_value_1 : false
      this.centroid_to_edge_value_2 = data.centroid_to_edge_value_2 ? data.centroid_to_edge_value_2 : false
      this.label_to_sealent_measurment = data.label_to_sealent_measurment ? data.label_to_sealent_measurment : false
      this.radius_defect_value = data.radius_defect_value
      this.left_radius = data.left_radius
      this.left_length = data.left_length
      this.right_radius = data.right_radius
      this.right_length = data.right_length
      this.defects = data.defects
      this.defect_list = data.ocr_barcode_mismatch
      this.acceptedCount = data.total_accepted
      this.rejectedCount = data.total_rejected
      this.totalCount = data.total
      this.threshold = data.alignment_values
      this.threshold_actual = data.actutal_alignment_values
    });
    this.isProcessRunning = true;
    this.metrixListInterval = setTimeout(() => {
      this.getMetrix();
    }, 1000);
  }


  goFullScreen(i: any) {
    //console.log(i.currentTarget.id[i.currentTarget.id.length - 1])
    //////console.log(i.currentTarget.id)
    var elem = document.getElementById(`full-view-${i.currentTarget.id.substring(22,)}`);

    if (elem.requestFullscreen) {
      elem.requestFullscreen();

      $(`#full-screen-icon-open-${i.currentTarget.id.substring(22,)}`).addClass("invisible")
      $(`#full-screen-icon-close-${i.currentTarget.id.substring(22,)}`).removeClass("invisible")
    }
  }

  exitFullScreen(i: any) {
    $(`#full-screen-icon-open-${i.currentTarget.id.substring(22,)}`).removeClass("invisible")
    $(`#full-screen-icon-close-${i.currentTarget.id.substring(22,)}`).addClass("invisible")
    this.cameraLayoutLoad()
    if (document.exitFullscreen) {
      document.exitFullscreen();
      console.log(i.currentTarget.id)

    }
  }



  getinspection() {
    this.inspection_payload = {
      "part_name": this.partafterSelect,
      "inspection_id": this.running_inspection_id
    }
    let inspectionData = 
    this.marutiService.getInspection(this.inspection_payload).pipe(
    );
    inspectionData.subscribe((data) => {
      this.Apicalldone = true;
      this.buttonText = "Please wait ..."
      // $("#inspect_btn").text
      this.inspectShow = true; 
      // this.addInvisibleClass();
      console.log("yes")
    })
  }


  setConfigurationFunction() {
    $("#configuration-model").modal("show")
  }


  loadsetConfigurationForm() {
    this.setConfiguration = this._fb.group({
      // workstation_id: ['', [Validators.required]],
      rows: ['', [Validators.required]],
      columns: ['', [Validators.required]],
      port: ['', [Validators.required]],
    });
  }

  submitModalConfiguration(model) {
    this.isSubmittedConfig = true

    //console.log(model)
    if (!model.valid) {
      this.alertService.alertMessage(
        'Enter valid details',
        'danger',
        'error'
      );
      return
    }

    let payload = {
      "row": model.value.rows,
      "columns": model.value.columns
    }
    localStorage.setItem("Port", model.value.port)
    this.marutiService.setConfig(payload).subscribe((data) => {
    })
    $("#configuration-model").modal("hide")
    setTimeout(() => {
      window.location.reload()
    }, 100);
  }

  editThreshold(e) {
      e.stopPropagation();
      $("#edit-threshold-modal").modal("show")
      this.showEditIcon = true
      this.thresholdForm.patchValue({
        top: this.threshold_actual.top_value,
        bottom: this.threshold_actual.bottom_value,
        left: this.threshold_actual.left_value,
        // right: this.threshold_actual.right_value,
      });

  }

  submitThreshold(model) {
    if (!model.valid) {
      this.alertService.alertMessage(
        'Enter valid details',
        'danger',
        'error'
      );
      return
    }
    // this.showEditIcon = !this.showEditIcon;

    //console.log(model)
    this.marutiService.setThreshold(model.value).subscribe((data) => {
      // this.threshold_actual = {
      //   top_value : model.value.top,
      //   bottom_value : model.value.bottom,
      //   left_value : model.value.left,
      //   right_value : model.value.right,
      // }
      this.alertService.alertMessage(
        'Allignment Values Updated Successfully'
        ,"success","check"
      );
      $("#edit-threshold-modal").modal("hide")
      this.showEditIcon = !this.showEditIcon;
    })

  }

  continuRobotMovenent(){
    // this.marutiService.getApi()
  }
  closeModal(){
    this.showEditIcon = false;
    console.log("i'm here");
    
  }

  addInvisibleClass(){
    $('#inspect_btn_ins').addClass('invisible');
    $('#inspect_btn_wait').removeClass('invisible');
  }

  removeInvisbleClass(){
    $('#inspect_btn_ins').removeClass('invisible');
    $('#inspect_btn_wait').addClass('invisible');
  }

  onChangeRange(rangeValue: any){
    this.marutiService.setThreshold({range : rangeValue}).subscribe((data) => {
    })
  }

}
