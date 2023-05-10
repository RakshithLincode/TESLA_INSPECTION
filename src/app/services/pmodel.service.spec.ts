import { TestBed } from '@angular/core/testing';

import { PmodelService } from './pmodel.service';

describe('PmodelService', () => {
  let service: PmodelService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PmodelService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
