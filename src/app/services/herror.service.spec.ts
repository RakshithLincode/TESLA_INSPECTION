import { TestBed } from '@angular/core/testing';

import { HerrorService } from './herror.service';

describe('HerrorService', () => {
  let service: HerrorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HerrorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
