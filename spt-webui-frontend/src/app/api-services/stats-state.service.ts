import { Injectable } from '@angular/core';
import { BehaviorSubject } from "rxjs";
import { ApiStats } from "./models";
import { SptWebUiApiWrapperService } from "./spt-web-ui-api-wrapper.service";

@Injectable({
	providedIn: 'root'
})
export class StatsStateService {

	private _currentStats: BehaviorSubject<ApiStats | null> = new BehaviorSubject<ApiStats | null>(null);
	currentStats$ = this._currentStats.asObservable();

	constructor(
		private apiWrapper: SptWebUiApiWrapperService
	) {
		// todo: update stats when new song is requested or something maybe idk what im thinking
		this.apiWrapper.getStats().subscribe({
			next: value => {
				this._currentStats.next(value);
			}
		});
	}
}
