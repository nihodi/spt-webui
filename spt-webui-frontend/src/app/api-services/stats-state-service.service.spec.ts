import { TestBed } from '@angular/core/testing';

import { StatsStateService } from './stats-state.service';

describe('StatsStateServiceService', () => {
  let service: StatsStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StatsStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
