import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AppPopularTracksListComponent } from './app-popular-tracks-list.component';

describe('AppPopularTracksListComponent', () => {
  let component: AppPopularTracksListComponent;
  let fixture: ComponentFixture<AppPopularTracksListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppPopularTracksListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AppPopularTracksListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
