import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LivisProfileComponent } from './livis-profile.component';

describe('LivisProfileComponent', () => {
  let component: LivisProfileComponent;
  let fixture: ComponentFixture<LivisProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LivisProfileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LivisProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
