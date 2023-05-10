import { Component, OnInit, ViewChild,ElementRef, OnDestroy,Input } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import {AlertService} from '../../../services/alert.service';
import {DefectreportService} from "../../../services/defectreport.service";
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import {OperatorService} from '../../../services/operator.service';
import * as moment from 'moment';

// import {DragDropModule} from '@angular/cdk/drag-drop';
declare const $: any;

@Component({
  selector: 'app-defect-details',
  templateUrl: './defect-details.component.html',
  styleUrls: ['./defect-details.component.css']
})
export class DefectDetailsComponent implements OnInit {

  constructor(private alertService:AlertService,
    private defectreportService:DefectreportService,
    private _fb: FormBuilder,
    private operatorService:OperatorService) {
    // this.fromDate = calendar.getToday();
    // this.toDate = calendar.getNext(calendar.getToday(), 'd', 10);
  }
  displayedColumns;
  dataSource: MatTableDataSource<any>;
  dataLength: number;
  remarkForm:FormGroup;
  searchForm:FormGroup;

  isSubmitted = false;
  defectList:any;
  featureList:any;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  selectedRowIndex: number = -1;
  ngOnInit(): void {
    this.loadRemarkForm();
    this.loadSearchForm();

    this.displayedColumns = ["slNo","operator","createdAt","partNumber","pluggedcell","serialNumber","Defects",
    "MissingFeature","operation"];
    
    this.getDefectReport();
    this.getdefectList();
    this.getFeatureList();
  }

  getDefectReport(start_date="",end_date="",defect_list="",feature_list="")
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
    if(defect_list)
    {
      reportfilter.defect_type = defect_list;
    }
    if(feature_list)
    {
      reportfilter.feature_type = feature_list;
    }
    this.defectreportService.getDefectReport(reportfilter)
    .subscribe(data =>{
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.data = data;
      this.dataLength = data.length;

      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }

  getdefectList()
  {
    this.defectreportService.getMasterDefectList()
        .subscribe(data =>{
      //  console.log(data)   
      this.defectList = data;
    })
  }

  getFeatureList()
  {
    this.defectreportService.getMasterFeatureList()
        .subscribe(data =>{
      //  console.log(data)   
      this.featureList = data;
    })
  }

  loadRemarkForm()
  {
    this.remarkForm = this._fb.group({
      process_id: ['', [Validators.required]],
      inseption_id: ['', [Validators.required]],
      remark: ['', [Validators.required]],
   });
  }

  loadSearchForm()
  {
    this.searchForm = this._fb.group({
      date_range: ['', [Validators.required]],
      feature_list: ['',],
      defect_list: ['', ],
   });
  }

  serachFilter(model)
  {
    this.isSubmitted = true;
    // console.log(this.searchForm.value);
    if(!this.searchForm.invalid){
     
      var start_date = model.value.date_range.start.format("YYYY-MM-DD HH:mm:ss");
      var end_date = model.value.date_range.end.format("YYYY-MM-DD HH:mm:ss");
      var defects = model.value.defect_list;
      var features = model.value.feature_list;
      // console.log(model.value);
      this.isSubmitted = false;
      this.getDefectReport(start_date,end_date,defects,features);
    }
    // var date_range = $("#date_range").val();
    // if(date_range){
    //   var date_range_arr = date_range.split("- ");
    //   // alert(date_range);
    //   console.log(date_range_arr);
    // }else{
    //   this.alertService.alertMessage("Please Select Date","danger","close");
    // }
  }

  showRemarkForm(process_id,inseption_id,remark="")
  {
    this.remarkForm.patchValue({
      process_id:process_id,
      inseption_id: inseption_id,
      remark: remark,
    });
    $("#add-remark-modal").modal("show");
  }

  updateRemark(model)
  {
    // console.log(model.value);
    this.isSubmitted = true;
    if(!this.remarkForm.invalid){
      this.isSubmitted = false;
      var ocr_info = {inspection_id:model.value.process_id,current_inspected_part_id:model.value.inseption_id,remark:model.value.remark};
        // this.defect_list.ocr_result = model.value.part_number;
        // this.operatorService.updateOcr(ocr_info)
        // .subscribe(data =>{
          $("#add-remark-modal").modal("hide");
          if(!this.searchForm.invalid){
            this.serachFilter(this.searchForm);
          }else{
            this.getDefectReport();
          }
          
          this.alertService.alertMessage("Remark Updated Successfully","success","check");
        // });
    }
  }
  parcePluggedCell= function(input){
      return ((parseFloat(input)).toFixed(4));
  }

  listSubstring= function(input){
    return (input.toString().substring(0,10));
  }

  transformArrayString(input)
  {
    return (input.toString());
  }

  dateTransformation(datatime)
  {
    return (moment(datatime).format('YYYY-MM-DD'));
  }

}
