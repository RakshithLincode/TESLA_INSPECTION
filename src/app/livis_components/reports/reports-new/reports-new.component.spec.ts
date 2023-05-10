import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportsNewComponent } from './reports-new.component';

describe('ReportsNewComponent', () => {
  let component: ReportsNewComponent;
  let fixture: ComponentFixture<ReportsNewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReportsNewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportsNewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
