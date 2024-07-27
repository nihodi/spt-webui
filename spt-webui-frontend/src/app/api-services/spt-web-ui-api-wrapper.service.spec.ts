import { TestBed } from '@angular/core/testing';

import { SptWebUiApiWrapperService } from './spt-web-ui-api-wrapper.service';

describe('SptWebUiApiWrapperService', () => {
	let service: SptWebUiApiWrapperService;

	beforeEach(() => {
		TestBed.configureTestingModule({});
		service = TestBed.inject(SptWebUiApiWrapperService);
	});

	it('should be created', () => {
		expect(service).toBeTruthy();
	});
});
