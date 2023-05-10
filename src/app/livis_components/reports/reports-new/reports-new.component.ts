import { Component, OnInit, ViewChild, ElementRef, OnDestroy, Input, ViewEncapsulation } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { AlertService } from '../../../services/alert.service';
import { DefectreportService } from "../../../services/defectreport.service";
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { OperatorService } from '../../../services/operator.service';
import * as moment from 'moment';
import { ShiftService } from 'src/app/services/shift.service';
import { WorkstationService } from 'src/app/services/workstation.service';
import { ManageUserService } from 'src/app/services/manage-user.service';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
declare var require: any;


declare const $: any;

@Component({
  selector: 'app-defect-details',
  templateUrl: './reports-new.component.html',
  styleUrls: ['./reports-new.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class ReportsNewComponent implements OnInit {
  livislogo: string;
  features: any;
  defects: any;
  cancel: string;
  tick: string;
  reject_reason_defects: any;
  reject_reason_features: any;
  currentLimit: any;
  currentPage: any = 0;
  printImage: any;
  fullScreenOn: boolean = true;
  isAdmin: boolean;
  part_list: any;
  isEmpty: boolean = true;

  constructor(
    private alertService: AlertService,
    private defectreportService: DefectreportService,
    private _fb: FormBuilder,
    private operatorService: OperatorService,
    private shiftService: ShiftService,
    private workstationService: WorkstationService,
    private manageUserService: ManageUserService,
    private marutiService: OperatorService,
  ) {
    this.filteredWorkStations = this.wsCtrl.valueChanges.pipe(
      startWith(''),
      map((value: string | null) => value ? this.filterWorkStations(value) : this.workStationNames.slice())
    )
  }

  shifts: any;
  isLoading = true;
  workstations: any;
  workStationNames = [];
  users: any;
  displayedColumns: any;
  dataSource: any;
  dataLength: number;
  remarkForm: FormGroup;
  searchForm: FormGroup;
  pageSize = 10;
  isSubmitted = false;
  resultsLength: number;
  selectedExperimentID: string;
  isInference = true;
  selectedDefect: any;
  selectedImage: any;
  selectedUrl: any;
  filterPayload: any;
  isFlagModal = false;
  wsCtrl = new FormControl()
  filteredWorkStations: Observable<string[]>

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  @ViewChild('workStationsInput') workStationsInput: ElementRef<HTMLInputElement>;
  @ViewChild('pdfTable')
  pdfTable!: ElementRef;
  selectedRowIndex = -1;
  ngOnInit(): void {
    this.filterPayload = {
      from_date: '',
      to_date: '',
      operator_id: '',
      shift_id: '',
      workstation_id: '',
      status: '',
      skip: 0,
      limit: this.pageSize,
      model : ''
    }
    this.loadRemarkForm();
    this.loadSearchForm();

    this.displayedColumns = [
      'slNo',
      // 'operator',
      'createdAt',
      'partNumber',
      // 'workstation',
      'status',
      // 'operation'
    ];

    // this.getUsers();
    // this.getWorkstations();
    this.livislogo = "../../../../assets/img/lincode_livis.png"
    this.cancel = "../../../../assets/img/cancel.svg"
    this.tick = "../../../../assets/img/confirm.svg"
    this.getDefectReport();
    let user_info = JSON.parse(localStorage.getItem('livis_user'));
        if (user_info && user_info['role_name']) {
            if (user_info['role_name'] == 'admin') {
                console.log(user_info['role_name'])
                this.isAdmin = true
            } else {
                this.isAdmin = false
            }
        }
        this.getPartList()
  }
  getPartList() {
    ////////console.log("INSIDE GET ALL PARTS")
    this.marutiService.getAllParts().subscribe((data) => {
      this.part_list = data;
      ////////console.log("GET ALL PARTS==============================>", this.part_list);

    });
  }

  getUsers(): void {
    this.manageUserService.getAllUsers().subscribe(response => {
      this.users = response;
    });
  }

  getWorkstations(): void {
    this.workstationService.getWorkStations().subscribe(response => {
      this.workstations = response;
      response.map((workstation: any) => {
        this.workStationNames.push(workstation.workstation_name)
      })
    });
  }

  filterWorkStations(value: string): string[] {
    const workStation = value.toLowerCase();
    return this.workStationNames.filter(ws => ws.toLowerCase().includes(workStation))
  }

  onFocus() {
    this.filteredWorkStations = this.wsCtrl.valueChanges.pipe(
      startWith(''),
      map((value: string | null) => value ? this.filterWorkStations(value) : this.workStationNames.slice())
    )
  }

  getDefectReport() {
    // //console.log(this.currentPage)
    this.currentPage = 1
    this.defectreportService.getDefectReport(this.filterPayload)
      .subscribe(data => {
        this.isLoading = false
        this.dataSource = data.data;
        this.resultsLength = data.total;

      });
  }

  loadRemarkForm() {
    this.remarkForm = this._fb.group({
      slave_obj_id: ['', [Validators.required]],
      //master_obj_id: ['', [Validators.required]],
      remark: ['', [Validators.required]],
      created_at: ['', [Validators.required]],
    });
  }

  loadSearchForm() {
    this.searchForm = this._fb.group({
      date_range: ['',],
      operator_id: ['',],
      shift_id: ['',],
      workstation_id: ['',],
      status: ['',],
      model : ['',]
    });
  }


  serachFilter(model: any): void {
    this.isLoading = true
    this.isSubmitted = true;
    let date_from = '';
    let date_to = '';
    if (model.value.date_range.start) {
      date_from = model.value.date_range.start.format('YYYY-MM-DD HH:mm:ss') || '';
      date_to = model.value.date_range.end.format('YYYY-MM-DD HH:mm:ss') || '';
    }
    this.filterPayload = {
      from_date: date_from,
      to_date: date_to,
      operator_id: model.value.operator_id,
      workstation_id: model.value.workstation_id,
      status: model.value.status,
      skip: 0,
      limit: this.currentLimit ? this.currentLimit : 10,
      model : model.value.model
      // skip: 0,
      // limit: this.pageSize,
    };
    // if (model.value.status == 'pass') {
    //   this.filterPayload.status = true
    // }
    // else if (model.value.status == 'fail') {
    //   this.filterPayload.status = false
    // }
    // else {
    //   this.filterPayload.status = ''
    // }

    if (this.wsCtrl.value) {
      this.workstations.map((workstation: any) => {
        if (workstation.workstation_name == this.wsCtrl.value) {
          this.filterPayload.workstation_id = workstation._id
        }
      })
      if (!this.filterPayload.workstation_id) {
        this.isLoading = false
        this.alertService.alertMessage('Please Select Valid WorkStation', 'danger', 'error')
        return;
      }
    }
    this.isSubmitted = false;
    this.paginator.firstPage()
    this.getDefectReport();
  }

  showRemarkForm(report: any) {
    this.remarkForm.patchValue({
      slave_obj_id: report._id,
      //master_obj_id: report._id,
      remark: report.remarks,
      created_at: report.created_at
    });
    $("#add-remark-modal").modal("show");
  }

  showFlagForm() {
    this.isFlagModal = true;
    this.remarkForm.patchValue({
      slave_obj_id: this.selectedDefect._id,
      //master_obj_id: this.selectedDefect._id,
      remark: this.selectedDefect.remarks,
      created_at: this.selectedDefect.created_at
    });
    $("#defect-image-modal").modal("hide")
    $("#add-remark-modal").modal("show");
  }

  showFlagFromViewForm(element) {
    this.isFlagModal = true;
    this.remarkForm.patchValue({
      slave_obj_id: element._id,
      //master_obj_id: this.selectedDefect._id,
      remark: element.remarks,
      created_at: element.created_at
    });
    $("#defect-image-modal").modal("hide")
    $("#add-remark-modal").modal("show");
  }

  // updateRemark(model) {
  //   this.isSubmitted = true;
  //   if (!this.remarkForm.invalid) {
  //     this.isSubmitted = false;
  //     this.defectreportService.addRemark(model.value)
  //       .subscribe(data => {
  //         $("#add-remark-modal").modal("hide");
  //         this.getDefectReport();

  //         this.alertService.alertMessage("Remark Updated Successfully", "success", "check");
  //       });
  //   }
  // }

  // updateFlag(model) {
  //   this.isSubmitted = true;
  //   //console.log("first")
  //   $("#update-remark").text("Please wait")
  //   $("#update-remark").attr("disabled", true)
  //   if (!this.remarkForm.invalid) {
  //     this.isSubmitted = false;

  //     this.defectreportService
  //       .updateFlagStatus(model.value)
  //       .subscribe((data) => {

  //         $("#update-remark").text("Update")
  //         $("#update-remark").removeAttr("disabled")
  //         this.isFlagModal = false;
  //         $('#add-remark-modal').modal('hide');
  //         this.getDefectReport();

  //         this.alertService.alertMessage(
  //           'Flagged Successfully',
  //           'success',
  //           'check'
  //         );
  //       });
  //   }
  // }

  // 
  // Helper Functions
  // 
  // parcePluggedCell= function(input){
  //     return ((parseFloat(input)).toFixed(4));
  // }
  // 
  // transformArrayString(input)
  // {
  //   return (input.toString());
  // }

  listSubstring = function (input) {
    return (input.toString().substring(0, 10)) + '...';
  }

  dateTransformation(datatime) {
    let date = new Date(datatime)
    date.setHours(date.getHours() + 5);
    date.setMinutes(date.getMinutes() + 30);
    return date.toLocaleString();
  }

  showDefectImageModal(defect: any): void {
    this.selectedDefect = defect;
    this.isInference = true;
    this.selectedImage = 'Inference Image'
    this.selectedUrl = defect.inference_frames
    // this.printImage = [...defect.input_frames, ...defect.inference_frames]
    this.printImage = [defect.captured_original_frame, defect.captured_inference_frame, defect.captured_mask_frame, defect.captured_measure_frame]
    console.log(this.printImage)

    // for LED 
    // this.features = this.selectedDefect.feature_list ? this.selectedDefect.feature_list : ["Orange Led", "Yellow Led"]
    // this.defects = ["crack_line","distortion", "excess_red","excess_material","damage"]
    // this.reject_reason_defects = this.selectedDefect.reject_reason ? this.selectedDefect.reject_reason.defects : this.selectedDefect.defect_list
    // this.reject_reason_features = this.selectedDefect.reject_reason ? this.selectedDefect.reject_reason.features : []
    console.log(this.selectedDefect.feature_list, this.selectedDefect.defect_list, this.selectedDefect.reject_reason)
    this.features = this.selectedDefect.feature_list ? this.selectedDefect.feature_list : []
    this.defects = this.selectedDefect.defect_list ? this.selectedDefect.defect_list : []
    this.reject_reason_defects = this.selectedDefect.reject_reason ? this.selectedDefect.reject_reason.defects : []
    this.reject_reason_features = this.selectedDefect.reject_reason ? this.selectedDefect.reject_reason.features : []
    // this.features = this.defects = this.reject_reason_defects = this.reject_reason_features = ["scratch", "dent", "scratch", "dom", "den", "scratch", "scratch", "scratch",]
    // this.reject_reason_defects = ["scratch", "den"]
    console.log(this.features, this.defects, this.reject_reason_defects, this.reject_reason_features)
    $("#defect-image-modal").modal('show')
  }

  changeImage(): void {
    if (this.isInference) {
      this.selectedImage = 'Original Image'
      this.selectedUrl = this.selectedDefect.input_frames
    }
    else {
      this.selectedImage = 'Inference Image'
      this.selectedUrl = this.selectedDefect.inference_frames
    }
  }

  gotoNextPage(event): void {
    // //console.log(event.pageSize)
    // this.isLoading = true
    // this.filterPayload.skip = event.pageIndex * event.pageSize;
    // this.filterPayload.limit = event.pageSize;
    // this.currentLimit = event.pageSize
    // this.getDefectReport();
    this.currentPage = event.pageIndex;
    this.filterPayload.skip = event.pageIndex * event.pageSize;
    this.filterPayload.limit = event.pageSize;
    // //console.log(this.dataLength);
    // //console.log(this.dataSource.data.length)
    this.getDefectReport();
  }

  printDiv(divName: any) {
    // var printContents = document.getElementById(divName).innerHTML;
    // var originalContents = document.body.innerHTML;
    // document.body.innerHTML = printContents;
    // window.print();     
    // document.body.innerHTML = originalContents;

    var divToPrint = document.getElementById(divName);
    var styles = `
    
    @font-face {
      font-family: LivisProximaFont;
      src: url(./assets/css/proxima/Proxima.otf);
    }
    body{
      justify-content : center;
      font-family: Calibri, sans-serif;

    }   
    .header{
      -webkit-print-color-adjust: exact; 
      color-adjust: exact; 
      background : #418ab3 !important;
      width:100% !important;
      height : 10vh !important;
      display: flex !important;
      justify-content : flex-start;
      align-items : end;
      color : #fff !important;
      font-size: 36px !important;
      padding-left: 5%;
      padding-bottom: 2%;
      letter-spacing: 3.0px;
      font-weight : 600 !important;
      text-transform : uppercase !important;
      font-family: Calibri, sans-serif;
    }
    .header2{
      position : fixed !important;
      top : 0px !important;
      -webkit-print-color-adjust: exact; 
      color-adjust: exact; 
      max-width:96% !important;
      min-width:96% !important;
      height : 5vh !important;
      display: flex !important;
      justify-content : flex-start;
      align-items : end;
      color : #000 !important;
      font-size: 30px !important;
      padding-bottom: 2%;
      letter-spacing: 3.0px;
      font-weight : 600 !important;
      text-transform : uppercase !important;
      font-family: Calibri, sans-serif;
      border-bottom : 1px solid #51697B !important;
      margin-inline : 2% !important
    }
    .livis-print-heading{
      font-family: Calibri !important;
    }
    .print_body{
      width: 100% !important;
    }
    .part_name{
      -webkit-print-color-adjust: exact; 
      color-adjust: exact; 
      display: flex !important;
      justify-content : flex-start !important;
      margin-inline : 2% !important;
      margin-block: 2.5vh !important;
      text-transform : capitalize;
      font-size: 16px !important;
      background : #f2f2f2 !important;
      color: #000 !important;
      font-weight : 600 !important;
      padding-block : 5px !important
    }
    .part_name_heading{
      -webkit-print-color-adjust: exact; 
      color-adjust: exact; 
      color : #51697B !important;
    }
    .print_img{
      width: 100% !important;
      height : 45% !important;
      
    }
    .print_img img{
      border-radius : 1.5rem !important;
      width : 48% !important;
      margin : 1% !important;
    }
    .print_details_heading{
      font-size: 16px !important;
      color : #51697B !important;
      margin-bottom : 5px !important
    }
    .print_details_body{
      font-size: 18px !important;
      font-weight : 700 !important;
      text-transform : capitalize !important
    }
    .print_details_sub_body{
      
      font-size: 18px !important;
      font-weight : 500 !important;
      text-transform : capitalize !important
    }


    .report-modal-status-rejected{
      font-weight: 700;
      font-size: 16px;
      color: #C90B0B;
  }
  .report-modal-status-accepted{
      color: #32BE0F;
      font-weight: 700;
      font-size: 16px;
  }
  .d-none{
    visibility : hidden !important
  }

  .hidden-tr,.hidden-tr td{
    padding-top : 300px !important;
    border:none !important;
    visibility:hidden !important;
  }
  .hidden-tr2,.hidden-tr2 td{
    padding-top : 1in !important;
    border:none !important;
    visibility:hidden !important;
  }
  .footer{
    position: fixed;
    bottom : 0px !important;
    left : 15px !important;
    display:flex;
    justify-content : center !important;
    margin-top : 5vh !important;

  }

  .footer1{
    position:relative;
    margin-top:1in;
  }
  .footer img{
    height : 25px !important
  }
  .cgr{
    position: relative;
    bottom:0px !important;
    left: 25%;
  }
  .d-flex{
    display : flex !important;
    flex-wrap : wrap !important
  }

  tr{
      border: 1px solid #a2a2a2;
      padding : 10px !important;
      page-break-inside:avoid;
      page-break-after:auto
  }
  .width-50{
    width : 50% !important
  }
  
  .remark-div{
    height : 80px !important
  }

  td{
    border: 1px solid #a2a2a2;
    vertical-align : baseline !important;
    padding : 5px 10px !important
  } 

  tr:nth-child(3),tr:nth-child(3) td{
    
  }


  table{
    margin-top : 2.5vh !important;
    min-width : 100% !important;
    page-break-inside:auto;
    border-collapse: collapse;
  }


 
  .defect-info{
    margin-top : 5px !important
  }
  .fd img{
    margin-left : 15px !important
  }
  .fd {
    display : flex !important;
    justify-content : flex-start !important;
    flex-wrap : wrap !important;
    align-items : center;
    min-width : 33.33% !important;
    width : 33.33% !important;
    max-width : 33.33% !important;
  }
  .twentyfive{
    min-width : 25% !important;
    width : 25% !important;
    max-width : 25% !important;
    margin-top : 15px !important;
  }
  
  .space-provider{
    width: max-content !important;
    flex-direction: column;
  }
  .info-td{
    max-width : 200px !important;
    width : 200px !important
  }

  .inspection_id{
    letter-spacing: 0px !important;
    font-size : 12px !important
  }
  .print_details_heading-ii{
    color : #51697B !important;

  }
  .j-c-b{
    justify-content : space-between !important
  }

  body{
    counter-reset: page;
  }
  .page-counter{
    position : fixed;
    right : 0px !important;
    bottom : 0px !important
  }
  .page-counter:after {
      counter-increment: page;
      content: "Page " counter(page);
  }
  .f-h-heading{
    padding-block : 15px !important
  }
  .f-h-subheading{
    padding-block : 5px !important
  }
  .f-h-subheadingtop{
    padding-block-end : 5px !important
  }

  .justify-evenly{
    justify-content : flex-start !important
  }

  .width-100{
    width : 100% !important
  }

  .align{
    display : flex !important ;
    justify-content : flex-start !important;
    align-items : center !important
  }
  .red{
    color : red !important
}

    `
    var newWin = window.open('', 'Print-Window');
    newWin.document.open();

    newWin.document.write(`<html><head><link rel="preconnect" href="https://fonts.googleapis.com">    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet"><style> ${styles} </style> </head><body onload="window.print()"> ${divToPrint.innerHTML}  </body></html>`);
    // newWin.document.write( divToPrint.innerHTML );
    newWin.document.title = "Livis_" + this.selectedDefect.created_at;
    newWin.print();
    // newWin.document.close();
    setTimeout(function () { newWin.close(); }, 100);
  }


  download(divName) {
    // const pdfTable = this.pdfTable.nativeElement;
    // //console.log(pdfTable)
    // var html = htmlToPdfmake(pdfTable.innerHTML);
    // const documentDefinition = { content: html };
    // setTimeout(() => {
    //   pdfMake.createPdf(documentDefinition).open();
    //   pdfMake.createPdf(documentDefinition).download();

    // }, 2000);
  }

  modalFullScreen() {

    if ($("#fullScreenDIV").hasClass("d-none")) {
      $("#fullScreenDIV").removeClass("d-none")
      $("#defect-image-modal").modal("hide");
      this.fullScreenOn = false
    } else {
      $("#fullScreenDIV").addClass("d-none")
      $("#defect-image-modal").modal("show")
      this.fullScreenOn = true
    }
  }
  CloseFullScreen() {
    $("#fullScreenDIV").addClass("d-none")
    $("#defect-image-modal").modal("hide");
    this.fullScreenOn = true

  }

  downloadReport(){
    this.defectreportService.downloadReport(this.filterPayload)
      .subscribe(data => {
        window.location.href = data
      })
  }

}