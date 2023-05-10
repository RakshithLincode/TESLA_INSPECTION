import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LivisLogoutComponent } from './livis-logout.component';

describe('LivisLogoutComponent', () => {
  let component: LivisLogoutComponent;
  let fixture: ComponentFixture<LivisLogoutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LivisLogoutComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LivisLogoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
