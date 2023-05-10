import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import swal from 'sweetalert2';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PmodelService } from "../../../services/pmodel.service";
import { AlertService } from '../../../services/alert.service';
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { ElementRef } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent, MatAutocomplete } from '@angular/material/autocomplete';
import { MatChipInputEvent } from '@angular/material/chips';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
declare const $: any;

@Component({
  selector: 'app-parts',
  templateUrl: './parts.component.html',
  styleUrls: ['./parts.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class PartsComponent implements OnInit {

  availables: any;
  features: any;
  defects: any;
  isLoading = true;
  partsForm: FormGroup;
  partsFormEdit: FormGroup;
  dataLength: number;
  isSubmitted = false;
  isSubmitedEdit = false;
  filterValue: any;
  skip: number = 0;
  displayedColumns = ['sl', 'model_number', 'model_description', 'defects', 'features',  'operation'];
  dataSource: any;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  visible = true;
  selectable = true;
  removable = true;
  separatorKeysCodes: number[] = [ENTER, COMMA];


  featureCtrl = new FormControl();
  EditfeatureCtrl = new FormControl();
  defectCtrl = new FormControl();
  EditdefectCtrl = new FormControl();



  filteredFeatures: Observable<string[]>;
  EditfilteredFeatures: Observable<string[]>;
  filteredDefects: Observable<string[]>;
  EditfilteredDefects: Observable<string[]>;

  Features: string[] = [];
  EditFeatures: string[] = [];
  Defects: string[] = [];
  EditDefects: string[] = [];

  allFeatures: string[] = [];
  EditallFeatures: string[] = [];
  allDefects: string[] = [];
  EditallDefects: string[] = [];


  @ViewChild('chipPartInput') chipPartInput: ElementRef<HTMLInputElement>;
  @ViewChild('auto') matAutocomplete: MatAutocomplete;






  constructor(private _fb: FormBuilder, private pmodelService: PmodelService,
    private alertService: AlertService) {

    this.filteredFeatures = this.featureCtrl.valueChanges.pipe(
      startWith(null),
      map((chipPart: string | null) => chipPart ? this._filterFeatures(chipPart) : this.allFeatures.slice()));
    this.EditfilteredFeatures = this.EditfeatureCtrl.valueChanges.pipe(
      startWith(null),
      map((chipPart: string | null) => chipPart ? this._filterEditFeatures(chipPart) : this.EditallFeatures.slice()));
    this.filteredDefects = this.defectCtrl.valueChanges.pipe(
      startWith(null),
      map((chipPart: string | null) => chipPart ? this._filterDefects(chipPart) : this.allDefects.slice()));
    this.EditfilteredDefects = this.EditdefectCtrl.valueChanges.pipe(
      startWith(null),
      map((chipPart: string | null) => chipPart ? this._filterEditDefects(chipPart) : this.EditallDefects.slice()));

  }
  private _filterFeatures(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.allFeatures.filter(chipPart => chipPart.toLowerCase().indexOf(filterValue) === 0);
  }
  private _filterEditFeatures(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.EditallFeatures.filter(chipPart => chipPart.toLowerCase().indexOf(filterValue) === 0);
  }

  private _filterDefects(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.allDefects.filter(chipPart => chipPart.toLowerCase().indexOf(filterValue) === 0);
  }
  private _filterEditDefects(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.EditallDefects.filter(chipPart => chipPart.toLowerCase().indexOf(filterValue) === 0);
  }


  addFeatures(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;
    // Add our chipPart  
    if ((value || '').trim()) {
      this.Features.push(value.trim());
    }
    // Reset the input value  
    if (input) {
      input.value = '';
    }
    this.featureCtrl.setValue(null);
  }
  removeFeatures(chipPart: string): void {
    const index = this.Features.indexOf(chipPart);
    if (index >= 0) {
      this.Features.splice(index, 1);
    }
  }


  EditaddFeatures(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;
    // Add our chipPart  
    if ((value || '').trim()) {
      this.EditFeatures.push(value.trim());
    }
    // Reset the input value  
    if (input) {
      input.value = '';
    }
    this.EditfeatureCtrl.setValue(null);
  }
  EditremoveFeatures(chipPart: string): void {
    const index = this.EditFeatures.indexOf(chipPart);
    if (index >= 0) {
      this.EditFeatures.splice(index, 1);
    }
  }


  addDefects(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;
    // Add our chipPart  
    if ((value || '').trim()) {
      this.Defects.push(value.trim());
    }
    // Reset the input value  
    if (input) {
      input.value = '';
    }
    this.defectCtrl.setValue(null);
  }
  removeDefects(chipPart: string): void {
    const index = this.Defects.indexOf(chipPart);
    if (index >= 0) {
      this.Defects.splice(index, 1);
    }
  }


  EditaddDefects(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;
    // Add our chipPart  
    if ((value || '').trim()) {
      this.EditDefects.push(value.trim());
    }
    // Reset the input value  
    if (input) {
      input.value = '';
    }
    this.EditdefectCtrl.setValue(null);
  }
  EditremoveDefects(chipPart: string): void {
    const index = this.EditDefects.indexOf(chipPart);
    if (index >= 0) {
      this.EditDefects.splice(index, 1);
    }
  }




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
    this.pmodelService.getModels()
      .subscribe(data => {
        // let data =[
        //   {
        //     _id : "12344",
        //     model_no : "1234567890",
        //     isCompleted : true
        //   },
        //   {
        //     _id : "121212",
        //     model_no : "1234567890",
        //     isCompleted : false
        //   },
        //   {
        //     _id : "111111",
        //     model_no : "1234567890",
        //     isCompleted : true
        //   },

        // ]
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.data = data;
        this.dataLength = data.length;
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
        this.isLoading = false;
      });

  }

  SetRegions(e) {
    window.location.href = `http://localhost:3000/singleAnnotate?id=${e.model_number}&Objectid=${e._id}`
  }

  loadAddForm() {
    this.partsForm = this._fb.group({
      model_number: ['',],
      model_description: ['',],
      part_type: ['', [Validators.required,]],
      part_name: ['', [Validators.required,]],
      features: ['',[] ],
      defects: ['', []]
    })
    this.Features = [];
    this.Defects = [];
  }


  loadEditForm() {
    this.partsFormEdit = this._fb.group({
      _id: ['', [Validators.required]],
      edit_model_number: ['',],
      edit_model_description: ['',],
      edit_part_type: ['', [Validators.required,]],
      edit_part_name: ['', [Validators.required,]],
      edit_features: ['', []],
      edit_defects: ['',[]]

    });
  }

  filterParts(value: string): void {
    console.log(value)
    this.dataSource.filter = value.trim().toLowerCase();
  }

  addParts() {
    this.partsForm.reset();
    this.loadAddForm();
    $("#add-part-modal").modal("show");
  }

  addNewPart(model) {
    console.log(model.value, this.Features, this.Defects)
    this.isSubmitted = true;
    if (!this.partsForm.invalid) {
      // console.log(model);
      if((this.Features.length>0) && (this.Defects.length>0)){

      model.value.availables = this.availables;
      model.value.features = this.features;
      model.value.defects = this.defects;
      // console.log(model.value);
      const payload = {
        ...model.value, features : this.Features, defects : this.Defects
      }
      this.pmodelService.addModel(payload)
        .subscribe(data => {
          this.alertService.alertMessage("Added Successfully", "success", "check");
        });
      this.isSubmitted = false;
      this.getModelList();
      this.loadAddForm();
      $("#add-part-modal").modal("hide");
      }else{
        this.alertService.alertMessage("Atleast One feature and defect is required","danger","close");
      $("#add-part-modal").modal("hide");
        return
      }
    }
  }

  editPart(id) {
    this.pmodelService.updateModel(id)
      .subscribe(data => {
        console.log(data);

        this.partsFormEdit.patchValue({
          _id: data._id,
          edit_part_name :data.select_model,
          edit_part_type :data.label_type,
        });
        this.EditFeatures = data.features
        this.EditDefects = data.defeats
        console.log(this.partsFormEdit.value);
        
        $("#edit-part-modal").modal("show");

      });

  }

  updatePartInfo(model) {
    // console.log(model.value, this.EditDefects, this.EditFeatures);
    // this.isSubmitedEdit = true;
    // if(!this.partsFormEdit.invalid){
      model.value.edit_defects = this.EditDefects
      model.value.edit_features = this.EditFeatures
      console.log(model.value);
      
    this.pmodelService.submitModel(model.value)
      .subscribe(data => {
        this.alertService.alertMessage("Updated Successfully", "success", "check");
        this.getModelList();
      });
    this.isSubmitedEdit = false;
    $("#edit-part-modal").modal("hide");
    // }
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
        this.pmodelService.deleteModel({ part_name : id })
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

}
