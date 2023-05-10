import { Component, OnInit, ViewChild,ElementRef, OnDestroy,Input } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import {ReportService} from "../../../services/report.service";
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as moment from 'moment';
import { AuthenticationService } from '../../../services/authentication.service';
// import '@angular/';
// import {MatDatepickerModule} from '@angular/material/datepicker';
// import {NgbDate, NgbCalendar,NgbInputDatepicker,NgbDateParserFormatter} from '@ng-bootstrap/ng-bootstrap';
declare const $: any;


@Component({
  selector: 'app-production-quality',
  templateUrl: './production-quality.component.html',
  styleUrls: ['./production-quality.component.css']
})
export class ProductionQualityComponent implements OnInit {
  isSubmitted=false;
searchForm:FormGroup;
operators:any;
workstations:{};

  constructor(private reportService:ReportService,
    private _fb: FormBuilder,
    private authenticationService:AuthenticationService) {
    // this.fromDate = calendar.getToday();
    // this.toDate = calendar.getNext(calendar.getToday(), 'd', 10);
  }
  displayedColumns;
  dataSource: MatTableDataSource<any>;
  dataLength: number;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  selectedRowIndex: number = -1;
  ngOnInit(): void {
    this.loadSearchForm();
    this.getWorkStations();
    this.getOperators();
    this.displayedColumns = ["slNo","createdAt","operatorName","accepted","rejected"];
    this.getDefectReport();
  }

  getWorkStations(): void {
    this.authenticationService.getWorkStations()
      .subscribe(workstations => this.workstations = workstations);
      // this.workstations = this.loginService.getWorkStations();
    }

    getOperators(): void {
      this.reportService.geOperators()
        .subscribe(operators => this.operators = operators);
        // this.workstations = this.loginService.getWorkStations();
      }
  
    loadSearchForm()
    {
      this.searchForm = this._fb.group({
        date_range: ['', [Validators.required]],
        Workstation_name: ['',],
        operator_name: ['',],

        
     });
    }
  

  getDefectReport(start_date="",end_date="",workstation_name="",operator_name="")
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
    if(operator_name)
    {
      reportfilter.operator_name = operator_name;
    }
 
 
    this.reportService.getProductionQualityReports(reportfilter)
    .subscribe(data =>{
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.data = data;
      this.dataLength = data.length;

      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
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
      var operator_name = model.value.operator_name;
      // console.log(operator_name);
    
      this.isSubmitted = false;
      this.getDefectReport(start_date,end_date,Workstation_name,operator_name);
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
    if(this.searchForm.controls.operator_name.value)
    {
      filter_details['operator_name']= this.searchForm.controls.operator_name.value;
    }
    if(this.searchForm.controls.date_range.value)
    {
      filter_details['start_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");
      filter_details['end_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");

    }
    // let reportfilter = {file_format:"xlsx"};
    this.reportService.downloadProductionQualityReports(filter_details)
    .subscribe(data =>{
      // console.log(data);
      window.location.href = data;
    });
   }

  

}
