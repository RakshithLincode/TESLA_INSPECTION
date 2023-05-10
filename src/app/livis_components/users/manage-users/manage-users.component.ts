import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { StorageService } from 'src/app/helpers/storage.service';
import { AlertService } from 'src/app/services/alert.service';
import { ManageUserService } from 'src/app/services/manage-user.service';
import swal from 'sweetalert2';

declare const $: any;

const ALLOWED_ROLES = {
  admin: [
    { value: 'admin', viewValue: 'Admin' },
    { value: 'supervisor', viewValue: 'Supervisor' },
    { value: 'line_manager', viewValue: 'Line Manager' },
    { value: 'operator', viewValue: 'Operator' },
  ],
  supervisor: [
    { value: 'line_manager', viewValue: 'Line Manager' },
    { value: 'operator', viewValue: 'Operator' },
  ],
  line_manager: [{ value: 'operator', viewValue: 'Operator' }],
  si_user: [
    { value: 'business_manager', viewValue: 'Business Manager' },
    { value: 'sales_executive', viewValue: 'Sales Executive' },
  ],
  business_manager: [
    { value: 'sales_executive', viewValue: 'Sales Executive' },
  ],
};

@Component({
  selector: 'app-manage-users',
  templateUrl: './manage-users.component.html',
  styleUrls: ['./manage-users.component.css'],
})
export class ManageUsersComponent implements OnInit {
  userForm: FormGroup;
  userEditForm: FormGroup;
  dataLength: number;
  isSubmitted = false;
  isSubmitedEdit = false;
  isLoading = true;
  displayedColumns = [
    'sl',
    'username',
    // 'first_name',
    // 'last_name',
    'email',
    'role_name',
    // 'user_address',
    // 'phone_number',
    'operation',
  ];
  dataSource: MatTableDataSource<any>;
  userInfo: any;
  filterValue: string;
  resultsLength: number;
  roles = [];
  itemsPerPage = 5;
  searchQuery: string;
  isPasswordMatching = false;
  eyeIcon1: boolean = true;
  eyeIcon2: boolean = true;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;

  constructor(
    private _fb: FormBuilder,
    private manageUserService: ManageUserService,
    private alertService: AlertService,
    private storageService: StorageService
  ) {
    if (this.storageService.getUserDetails() && this.storageService.getUserDetails().role_name) {
      const roleName = storageService.getUserDetails().role_name;
      this.roles = [
        { value: 'admin', viewValue: 'Admin' },
        { value: 'operator', viewValue: 'Operator' },
      ]
    }
  }

  ngOnInit(): void {
    this.userInfo = this.storageService.getUserDetails();

    this.loadAddForm();
    this.loadEditForm();
    this.getUsers();
  }

  loadAddForm() {
    this.userForm = this._fb.group({
      username: ['', [Validators.required]],
      first_name: ['', [Validators.required]],
      // last_name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      role_name: ['', [Validators.required]],
      // user_address: ['', [Validators.required]],
      // phone_number: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.pattern(/^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/)]],
      confirm_password: ['', [Validators.required]],
      is_staff: [true],
      is_superuser: [false],
    });
  }

  loadEditForm() {
    this.userEditForm = this._fb.group({
      user_id: ['', [Validators.required]],
      username: [{ value: '', disabled: true }, [Validators.required]],
      first_name: ['', [Validators.required]],
      // last_name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      role_name: ['', [Validators.required]],
      // user_address: ['', [Validators.required]],
      // phone_number: ['', [Validators.required]],
      password: ['',[Validators.required, Validators.pattern(/^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/)]],
      confirm_password: [''],
      is_staff: [true],
      is_superuser: [false],
    });
  }

  getUsers(): void {
    this.manageUserService.getUsers(this.itemsPerPage).subscribe((response) => {
      this.isLoading = false;
      this.resultsLength = response.length
      this.dataSource = new MatTableDataSource(response);
      this.dataSource.data = response.map((data) => {
        let user: any;
        user = data.fields;
        user.user_id = data.pk;
        return user;
      });
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }

  showAddUserModal() {
    $('#add-user-modal').modal('show');
  }

  search(evt: any): void {
    this.searchQuery = evt.target.value;
    if (this.searchQuery.length < 3) {
      return;
    }

    this.manageUserService
      .searchUser(this.searchQuery, this.itemsPerPage)
      .subscribe((response) => {
        this.dataSource = response;
      });
  }

  filterShift(value: string): void {
    this.dataSource.filter = value.trim().toLowerCase();
  }

  addNewUser(model: FormGroup) {
    this.isSubmitted = true;
    console.log(model.value);
    this.isPasswordMatching =
      model.value.password === model.value.confirm_password;
    console.log(this.isPasswordMatching);
    console.log(this.userForm.invalid);
    $("#add-client-submit-btn").attr("disabled", true);

    if (this.userForm.invalid) {
      return;
    }

    if (!this.isPasswordMatching) {
      return;
    }

    this.isSubmitted = false;
    this.manageUserService.addNewUser(model.value).subscribe((data) => {
      $("#add-client-submit-btn").attr("disabled", false);

      this.alertService.alertMessage('Added Successfully', 'success', 'check');
      this.loadAddForm();
      $('#add-user-modal').modal('hide');
      this.getUsers();
    });
  }

  editUser(user: any) {
    $('#edit-user-modal').modal('show');

    this.userEditForm.patchValue({
      user_id: user.user_id,
      username: user.username,
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      role_name: user.role_name,
      user_address: user.user_address,
      phone_number: user.phone_number,
      is_staff: user.is_staff,
      is_superuser: user.is_superuser,
    });
  }

  updateUserInfo(model: FormGroup) {
    this.isSubmitedEdit = true;

    if (this.userEditForm.invalid) {
      return;
    }
    $("#update-client-submit-btn").attr("disabled", true);

    this.isSubmitedEdit = false;

    this.manageUserService.updateUser(model.value).subscribe((data) => {
      console.log(data);
      $("#update-client-submit-btn").attr("disabled", false);

      this.alertService.alertMessage(
        'Updated Successfully',
        'success',
        'check'
      );

      $('#edit-user-modal').modal('hide');
      this.getUsers();
      this.loadEditForm();
    });
  }

  deleteUser(user_id: string) {
    swal({
      title: 'Are you sure?',
      text: 'You will not be able to recover this parts!',
      type: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, keep it',
      confirmButtonClass: 'btn btn-success',
      cancelButtonClass: 'btn btn-danger',
      buttonsStyling: false,
    }).then((result) => {
      if (result.value) {
        this.manageUserService.deleteUser(user_id).subscribe((data) => {
          this.getUsers();
          swal({
            title: 'Deleted!',
            text: 'Your parts info has been deleted.',
            type: 'success',
            confirmButtonClass: 'btn btn-success',
            buttonsStyling: false,
          }).catch(swal.noop);
        });
      } else {
        swal({
          title: 'Cancelled',
          text: 'Your parts info is safe :)',
          type: 'error',
          confirmButtonClass: 'btn btn-info',
          buttonsStyling: false,
        }).catch(swal.noop);
      }
    });
  }

  gotoNextPage(evt: any) {
    this.itemsPerPage = evt.pageSize;
    this.manageUserService
      .getFilteredUsers(this.searchQuery, this.itemsPerPage, evt.pageIndex + 1)
      .subscribe((response) => {
        this.dataSource = response.map((data) => {
          let user: any;
          user = data.fields;
          user.user_id = data.pk;

          return user;
        });
      });
  }
  eyePressed1() {
    this.eyeIcon1 = !this.eyeIcon1
  }

  eyePressed2() {
    this.eyeIcon2 = !this.eyeIcon2
  }
}
