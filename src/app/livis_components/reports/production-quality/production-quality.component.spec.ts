import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductionQualityComponent } from './production-quality.component';

describe('ProductionQualityComponent', () => {
  let component: ProductionQualityComponent;
  let fixture: ComponentFixture<ProductionQualityComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProductionQualityComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductionQualityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
