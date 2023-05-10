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
  selector: 'app-defect-types',
  templateUrl: './defect-types.component.html',
  styleUrls: ['./defect-types.component.css']
})

export class DefectTypesComponent implements OnInit {

// @ViewChild('datePicker') datePicker: NgbInputDatepicker;
// fromDate: NgbDate;
// toDate: NgbDate;
// onFirstSelection = true;
isSubmitted=false;
searchForm:FormGroup;
workstations:{};

  // fromDate: NgbDate;
  // toDate: NgbDate;
  // hoveredDate: NgbDate;

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
    this.displayedColumns = ["slNo","defectType","quantity","operation"];
    this.loadSearchForm();
    this.getDefectReport();
    this.getWorkStations();
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
      lot_number: ['',],
   });
  }

  getDefectReport(start_date="",end_date="",workstation_name="",lot_number="")
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

    if(lot_number)
    {
      reportfilter.lot_number = lot_number;
    }
 
    this.reportService.getDefectTypeReports(reportfilter)
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
  //     id: 1,
  //     defect_type: 'Plugged Cell',
  //     quantity: '5', 
  //     },
  //     {
  //       id: 2,
  //       defect_type: 'Missing Lot Mark',
  //       quantity: '14', 
  //     }
  // ];
  //   this.dataSource = new MatTableDataSource(data);
  // }

  viewDefectDetails(id,element)
  {
    console.log(this.searchForm.controls.Workstation_name.value);
    let filter_details={};
    filter_details['defect_type']=element.defect_type;
    if(this.searchForm.controls.Workstation_name.value)
    {
      filter_details['Workstation_name']= this.searchForm.controls.Workstation_name.value;
    }
    if(this.searchForm.controls.date_range.value)
    {
      filter_details['start_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");
      filter_details['end_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");

    }
    // var start_date = this.searchForm.value.date_range.start.format("YYYY-MM-DD HH:mm:ss");
    // var end_date = model.value.date_range.end.format("YYYY-MM-DD HH:mm:ss");
    // var Workstation_name = model.value.Workstation_name;
    this.reportService.getDefectTypeDetailsReports(filter_details)
    .subscribe(data =>{
      var html = ``;
      if(data.length > 0)
      {
        $.each(data,(index,value)=>{
          // console.log(index,value);
          html += `<tr>
            <td>${(index+1)}</td>
            <td>${value.timestamp}</td>
            <td>${value.operator_name}</td>
            <td>${value.workstation_name}</td>

          </tr>`;
        })
        // html += ``;
      }else{
        html += `<tr>
        <td colspan="4" class="text-center">Data Not Found!!</td> 
        </tr>`;
      }
   
      // console.log(data);
      $("#defect-details-body").html(html);
      $("#defect-report-table").css({width:"30%"});
      $("#defect-report-table").addClass("table-right-border");
      $(".defect-detail-table-wrap").css({width:"70%"});
      this.displayedColumns = ["slNo","defectTypeNew"];
      this.selectedRowIndex = id;
      $(".defect-detail-table-wrap").removeClass('invisible-element');
      $(id).addClass('invisible-element');
    });
   
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
    this.displayedColumns = ["slNo","defectType","quantity","operation"];
    $(".defect-detail-table-wrap").addClass('invisible-element');

  }

  serachFilter(model)
  {
    this.isSubmitted = true;
    console.log(model.value);
    if(!this.searchForm.invalid){
     
      var start_date = model.value.date_range.start.format("YYYY-MM-DD HH:mm:ss");
      var end_date = model.value.date_range.end.format("YYYY-MM-DD HH:mm:ss");
      var Workstation_name = model.value.Workstation_name;
      var lot_number = model.value.lot_number;

    
      this.isSubmitted = false;
      this.getDefectReport(start_date,end_date,Workstation_name,lot_number);
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

    if(this.searchForm.controls.lot_number.value)
    {
      filter_details['lot_number']= this.searchForm.controls.lot_number.value;
    }
    if(this.searchForm.controls.date_range.value)
    {
      filter_details['start_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");
      filter_details['end_date']= this.searchForm.controls.date_range.value.start.format("YYYY-MM-DD HH:mm:ss");

    }
    // let reportfilter = {file_format:"xlsx"};
    this.reportService.downloadDefectTypeReports(filter_details)
    .subscribe(data =>{
      // console.log(data);
      window.location.href = data;
    });
   }
  

  // onDateSelection(date: NgbDate) {
  //   console.log(this.fromDate)

  //   if (!this.fromDate && !this.toDate) {
  //     this.fromDate = date;
  //   } else if (this.fromDate && !this.toDate && date.after(this.fromDate)) {
  //     this.toDate = date;
  //   } else {
  //     this.toDate = null;
  //     this.fromDate = date;
  //   }
  //   console.log(this.toDate)

  // }
  // isHovered(date: NgbDate) {
  //   return this.fromDate && !this.toDate && this.hoveredDate && date.after(this.fromDate) && date.before(this.hoveredDate);
  // }

  // isInside(date: NgbDate) {
  //   return date.after(this.fromDate) && date.before(this.toDate);
  // }

  // isRange(date: NgbDate) {
  //   return date.equals(this.fromDate) || date.equals(this.toDate) || this.isInside(date) || this.isHovered(date);
  // }

}
