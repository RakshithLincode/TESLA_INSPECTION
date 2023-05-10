import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ShiftSummaryComponent } from './shift-summary.component';

describe('ShiftSummaryComponent', () => {
  let component: ShiftSummaryComponent;
  let fixture: ComponentFixture<ShiftSummaryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ShiftSummaryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ShiftSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
