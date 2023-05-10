import { Component, OnInit, ViewChild,ElementRef, OnDestroy,Input } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import {ReportService} from "../../../services/report.service";
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as moment from 'moment';
import { AuthenticationService } from '../../../services/authentication.service';
import {ShiftService} from "../../../services/shift.service";
// import '@angular/';
// import {MatDatepickerModule} from '@angular/material/datepicker';
// import {NgbDate, NgbCalendar,NgbInputDatepicker,NgbDateParserFormatter} from '@ng-bootstrap/ng-bootstrap';
declare const $: any;


@Component({
  selector: 'app-shift-summary',
  templateUrl: './shift-summary.component.html',
  styleUrls: ['./shift-summary.component.css']
})
export class ShiftSummaryComponent implements OnInit {

  constructor(private reportService:ReportService,
    private _fb: FormBuilder,
    private authenticationService:AuthenticationService,
    private shiftService:ShiftService) {
    // this.fromDate = calendar.getToday();
    // this.toDate = calendar.getNext(calendar.getToday(), 'd', 10);
  }
  isSubmitted=false;
searchForm:FormGroup;
workstations:{};
shift_list:any;
  displayedColumns;
  dataSource: MatTableDataSource<any>;
  dataLength: number;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  selectedRowIndex: number = -1;
  ngOnInit(): void {
    this.loadSearchForm();
    this.getWorkStations();
    this.getShiftList();
    this.displayedColumns = ["slNo","createdAt","operatorName","accepted","rejected"];
    this.getDefectReport();
  }

  getShiftList()
  {
    this.shiftService.getShifts()
    .subscribe(data =>{
      this.shift_list = data;
    });
  }

  getWorkStations(): void {
    this.authenticationService.getWorkStations()
      .subscribe(workstations => this.workstations = workstations);
      // this.workstations = this.loginService.getWorkStations();
    }
  
    loadSearchForm()
    {
      this.searchForm = this._fb.group({
        date_range: ['', [Validators.required]],
        Workstation_name: ['',],
        shift_name: ['',],        
     });
    }

  getDefectReport(start_date="",end_date="",workstation_name="",shift_name="")
  {
    var reportfilter:any = {};
    if(start_date)
    {
      reportfilter.from_date = start_date;
    }
    if(end_date)
    {
      reportfilter.to_date = end_date;
    }
    if(workstation_name)
    {
      reportfilter.workstation_name = workstation_name;
    }

    if(shift_name)
    {
      reportfilter.shift_name = shift_name;
    }
 
 
    this.reportService.getShiftReports(reportfilter)
    .subscribe(data =>{
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.data = data;
      this.dataLength = data.length;

      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;

  //     const blob = new Blob([data], { type: 'pdf' });
  // const url= window.URL.createObjectURL(blob);
  // window.open(url);
    });
  }

 

  // getDefectReport()
  // {
  //   let data =  [
  //     {
  //       id: 1,
  //       created_at: '2020-10-10',
  //       operater_name: 'manjunath',
  //       accepted: 200, 
  //       rejected: 2, 
  //     },
  //     {
  //       id: 2,
  //       created_at: '2020-10-10',
  //       operater_name: 'manjunath',
  //       accepted: 200, 
  //       rejected: 2, 
  //     }
  // ];
  //   this.dataSource = new MatTableDataSource(data);
  // }

  viewDefectDetails(id,element)
  {
    var html = `  <tr>
    <td colspan="5" class="text-center">Data Not Found!!</td> 
    </tr>`;
    $("#defect-details-body").html(html);
    $("#defect-report-table").css({width:"30%"});
    $("#defect-report-table").addClass("table-right-border");
    $(".defect-detail-table-wrap").css({width:"70%"});
    this.displayedColumns = ["slNo","defectTypeNew"];
    this.selectedRowIndex = id;
    $(".defect-detail-table-wrap").removeClass('invisible-element');
    $(id).addClass('invisible-element');
  }



// highlight(row){
//     console.log(row);
//     this.selectedRowIndex = row.id;
// }
  backNormal()
  {
    this.selectedRowIndex = -1;
    $("#defect-report-table").css({width:"100%"});
    $("#defect-report-table").removeClass("table-right-border");
    this.displayedColumns = ["slNo","createdAt","operatorName","accepted","rejected","operation"];
    // this.displayedColumns = ["slNo","defectType","quantity","operation"];
    $(".defect-detail-table-wrap").addClass('invisible-element');

  }

  serachFilter(model)
  {
    this.isSubmitted = true;
    console.log(model.value);
    if(!this.searchForm.invalid){
     
      var start_date = model.value.date_range.start.format("YYYY-MM-DD HH:mm:ss");
      var end_date = model.value.date_range.end.format("YYYY-MM-DD HH:mm:ss");
      var Workstation_name = model.value.Workstation_name?model.value.Workstation_name:null;
      var shift_name = model.value.shift_name?model.value.shift_name:null;
    
      this.isSubmitted = false;
      this.getDefectReport(start_date,end_date,Workstation_name,shift_name);
    }
   
  }


  downloadReport()
  {
    // alert("ss");
    let filter_details={};
    filter_details['file_format']="xlsx";
    if(this.searchForm.controls.Workstation_name.value)
    {
      filter_details['Workstation_name']= this.searchForm.controls.Workstation_name.value;
    }
    if(this.searchForm.controls.shift_name.value)
    {
      filter_details['shift_name']= this.searchForm.controls.shift_name.value;
    }
    if(this.searchForm.controls.date_range.value)
    {
      filter_details['start_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");
      filter_details['end_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");

    }
    // let reportfilter = {file_format:"xlsx"};
    this.reportService.downloadShiftReports(filter_details)
    .subscribe(data =>{
      // console.log(data);
      window.location.href = data;
    });
   }


}
