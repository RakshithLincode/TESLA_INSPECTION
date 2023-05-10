import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DefectTypesComponent } from './defect-types.component';

describe('DefectTypesComponent', () => {
  let component: DefectTypesComponent;
  let fixture: ComponentFixture<DefectTypesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DefectTypesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DefectTypesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
