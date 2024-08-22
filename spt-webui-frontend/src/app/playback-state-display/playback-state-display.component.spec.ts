import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaybackStateDisplayComponent } from './playback-state-display.component';

describe('PlaybackStateDisplayComponent', () => {
  let component: PlaybackStateDisplayComponent;
  let fixture: ComponentFixture<PlaybackStateDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaybackStateDisplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlaybackStateDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
