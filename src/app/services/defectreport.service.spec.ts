import { TestBed } from '@angular/core/testing';

import { DefectreportService } from './defectreport.service';

describe('DefectreportService', () => {
  let service: DefectreportService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DefectreportService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
