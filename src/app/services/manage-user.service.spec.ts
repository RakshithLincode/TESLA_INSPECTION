import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ManageUserService } from './manage-user.service';

describe('ManageUserService', () => {
  let service: ManageUserService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule
      ]
    });
    service = TestBed.inject(ManageUserService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
