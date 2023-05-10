import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OperatorNewComponent } from './operator-new.component';

describe('OperatorNewComponent', () => {
  let component: OperatorNewComponent;
  let fixture: ComponentFixture<OperatorNewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OperatorNewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OperatorNewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
