import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import swal from 'sweetalert2';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PmodelService } from "../../../services/pmodel.service";
import { AlertService } from '../../../services/alert.service';
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';

import * as XLSX from 'xlsx';
import { COMMA, ENTER, SPACE } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material/chips';
import { ActivatedRoute } from '@angular/router';

declare const $: any;
@Component({
  selector: 'app-master-file',
  templateUrl: './master-file.component.html',
  styleUrls: ['./master-file.component.css'],
  encapsulation: ViewEncapsulation.None

})
export class MasterFileComponent implements OnInit {
  availables: any;
  features: any;
  defects: any;
  isLoading = true;
  partsForm: FormGroup;
  partsFormEdit: FormGroup;
  dataLength: number;
  isSubmitted = false;
  isSubmitedEdit = false;
  fileToUpload: File | null = null;
  filterValue : any
  displayedColumns =
    ['sl',
    'eu_number',
      'model_number',
      'description',
      // 'part_number',
      'amount',
      'unit',
      'uom',
      'country'
      //  'status', 'operation'
    ];
  //   test_data =  [{
  //     id: 1,
  //     model_number: 'Netgear Cable Modem',
  //     part_number: 'CM700',

  // },
  // {
  //     id: 2,
  //     model_number: 'Linksys Cable Modem',
  //     part_number: 'LK700',
  // }];
  dataSource: any;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  imageDisplay: string | ArrayBuffer;
  fileBlob: any;
  doneUploading: boolean = true;
  skip: number = 0;


  constructor(private _fb: FormBuilder, private pmodelService: PmodelService,
    private alertService: AlertService) { }

  ngAfterViewInit() {
    // console.log(this.paginator);
    // this.dataSource.paginator = this.paginator;
    // this.dataSource.sort = this.sort;
    // console.log(this.dataSource);
  }
  ngOnInit(): void {
    this.loadAddForm();
    this.loadEditForm();
    this.getModelList();
    var model_info = { "features": ["single_ringmark", "brown", "lotmark", "arrow", "model_no"], "model_no": "ca8", "plugged_cell_percent": 2.5 };
    this.availables = model_info.features;
    this.features = [];
    this.defects = [];

    // console.log(this.availables);
  }
  gotoNextPage(event): void {
    // this.isLoading = true
    this.skip = event.pageIndex * event.pageSize;
    // this.filterPayload.limit = event.pageSize;
    // this.currentLimit = event.pageSize
    // this.getDefectReport();
  }
  getModelList() {
    this.pmodelService.getBulk()
      .subscribe(data => {
        // let data = [
        //   {
        //     _id: "12344",
        //     model_no: "1234567890",
        //     isCompleted: true,
        //     amount: 20000,
        //     unit: 5,
        //     country: 'France'
        //   },
        //   {
        //     _id: "121212",
        //     model_no: "1234567890",
        //     isCompleted: false,
        //     amount: 20000,
        //     unit: 5,
        //     country: 'China'

        //   },
        //   {
        //     _id: "111111",
        //     model_no: "1234567890",
        //     isCompleted: true,
        //     amount: 20000,
        //     unit: 5,
        //     country: 'France'

        //   },

        // ]
        console.log(data)
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.data = data;
        this.dataLength = data.length;
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        this.isLoading = false;
      });

  }

  SetRegions(e) {
    window.location.href = `http://localhost:3000/annotate?id=${e._id}`
  }

  loadAddForm() {
    this.partsForm = this._fb.group({
      // part_number: ['', [Validators.required]],
      model: ['', [Validators.required,]],
      // bath_number_denominator: ['', [Validators.required, ]],
      // plugged_cell_percent: ['', [Validators.required,Validators.pattern(/^\d+(\.\d+)*$/), ]],

    });
  }


  loadEditForm() {
    this.partsFormEdit = this._fb.group({
      _id: ['', [Validators.required]],
      // edit_part_number: ['', [Validators.required]],
      edit_model: ['', [Validators.required,]],
      // edit_bath_number_denominator: ['', [Validators.required, ]],
    });
  }

  filterParts(value: string): void {
    console.log(value)
    this.dataSource.filter = value.trim().toLowerCase();
  }

  addParts() {
    $("#add-part-modal").modal("show");
  }

  addNewPart(model) {
    this.isSubmitted = true;
    if (!this.partsForm.invalid) {
      // console.log(model);
      // if((this.features.length>0) && (this.defects.length>0)){

      // model.value.availables = this.availables;
      // model.value.features = this.features;
      // model.value.defects = this.defects;
      // console.log(model.value);
      this.pmodelService.addModel(model.value)
        .subscribe(data => {
          this.alertService.alertMessage("Added Successfully", "success", "check");
        });
      this.isSubmitted = false;
      this.getModelList();
      this.loadAddForm();
      $("#add-part-modal").modal("hide");
      // }else{
      //   this.alertService.alertMessage("Atleast One feature and defect enable required","danger","close");
      // }
    }
  }

  editPart(id) {
    this.pmodelService.getModel(id)
      .subscribe(data => {
        // console.log(data);

        this.partsFormEdit.patchValue({
          _id: data._id,
          edit_model: data.model,
          edit_part_number: data.part_number,
          edit_bath_number_denominator: data.bath_number_denominator
        });
        $("#edit-part-modal").modal("show");

      });

  }

  updatePartInfo(model) {
    // console.log(model.value);
    this.isSubmitedEdit = true;
    if (!this.partsFormEdit.invalid) {
      this.pmodelService.updateModel(model.value)
        .subscribe(data => {
          this.alertService.alertMessage("Updated Successfully", "success", "check");
        });
      this.isSubmitedEdit = false;
      this.getModelList();
      $("#edit-part-modal").modal("hide");
    }
  }

  deletePartInfo(id) {
    swal({
      title: 'Are you sure?',
      text: 'You will not be able to recover this parts!',
      type: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, keep it',
      confirmButtonClass: "btn btn-success",
      cancelButtonClass: "btn btn-danger",
      buttonsStyling: false
    }).then((result) => {
      if (result.value) {
        this.pmodelService.deleteModel({ _id: id })
          .subscribe(data => {
            this.getModelList();
            swal({
              title: 'Deleted!',
              text: 'Your parts info has been deleted.',
              type: 'success',
              confirmButtonClass: "btn btn-success",
              buttonsStyling: false
            }).catch(swal.noop)

          });

      } else {
        swal({
          title: 'Cancelled',
          text: 'Your parts info is safe :)',
          type: 'error',
          confirmButtonClass: "btn btn-info",
          buttonsStyling: false
        }).catch(swal.noop)
      }
    })
  }


  drop(event: CdkDragDrop<string[]>) {
    console.log(this.availables); console.log(this.features); console.log(this.defects);
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex);
    }
  }

  uploadComponents() {
    $('#add-bulk-modal').modal('show');
  }

  // onFileChange(ev: any) {
  //   let workBook = null;
  //   let jsonData = null;
  //   const reader = new FileReader();
  //   const file = ev.target.files[0];
  //   console.log(file)
  //   console.log(file.blob)
  //   reader.onload = (event: any) => {
  //     const data = reader.result;
  //     workBook = XLSX.read(data, { type: 'binary' });
  //     console.log(workBook)
  //     jsonData = workBook.SheetNames.reduce((initial, name) => {
  //       const sheet = workBook.Sheets[name];
  //       initial[name] = XLSX.utils.sheet_to_json(sheet);
  //       return initial;
  //     }, {});


  //     console.log("json", jsonData)
  //   }
  //   reader.readAsBinaryString(file);


  //   const reader = new FileReader();
  //   reader.readAsDataURL(ev.target.files[0]);
  //   reader.onload = () =>{
  //     this.imageDisplay = reader.result;
  //     console.log(this.imageDisplay)
  //   }


  // }

  onFileChange(event) {
    if (event.target.value) {
      const file = event.target.files[0];
      const type = file.type;
      console.log(type)
      this.changeFile(file).then((base64: string): any => {
        console.log(base64);
        this.fileBlob = this.base64ToBlob([base64]);
        console.log(this.fileBlob)
      });
    } else alert('Nothing')
  }
  changeFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  }

  public base64ToBlob(b64Data, sliceSize = 512) {
    let byteCharacters = atob(b64Data); //data.file there
    let byteArrays = [];
    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      let slice = byteCharacters.slice(offset, offset + sliceSize);

      let byteNumbers = new Array(slice.length);
      for (var i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      let byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }
    return new Blob(byteArrays, { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    console.log(this.fileToUpload)
  }
  uploadFileToActivity() {
    this.doneUploading = false
    this.pmodelService.postFile(this.fileToUpload).subscribe(data => {
    this.doneUploading = true
      // do something, if upload success
      this.alertService.alertMessage("Uploaded Successfully", "success", "check");

      $("#add-bulk-modal").modal("hide")
    }, error => {
      console.log(error);
    });
  }


}
