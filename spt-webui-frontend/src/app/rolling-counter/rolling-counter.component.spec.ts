import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RollingCounterComponent } from './rolling-counter.component';

describe('RollingCounterComponent', () => {
  let component: RollingCounterComponent;
  let fixture: ComponentFixture<RollingCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RollingCounterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RollingCounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
