import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LivisLoginComponent } from './livis-login.component';

describe('LivisLoginComponent', () => {
  let component: LivisLoginComponent;
  let fixture: ComponentFixture<LivisLoginComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LivisLoginComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LivisLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
