import { TestBed } from '@angular/core/testing';

import { MarutiOperatorService } from './maruti-operator.service';

describe('MarutiOperatorService', () => {
  let service: MarutiOperatorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MarutiOperatorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
