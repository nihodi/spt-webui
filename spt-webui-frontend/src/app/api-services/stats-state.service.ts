import { Injectable } from '@angular/core';
import { BehaviorSubject } from "rxjs";
import { ChartableApiStats } from "./models";
import { SptWebUiApiWrapperService } from "./spt-web-ui-api-wrapper.service";
import { ChartConfiguration } from "chart.js";

@Injectable({
	providedIn: 'root'
})
export class StatsStateService {

	private _currentStats: BehaviorSubject<ChartableApiStats | null> = new BehaviorSubject<ChartableApiStats | null>(null);
	currentStats$ = this._currentStats.asObservable();

	constructor(
		private apiWrapper: SptWebUiApiWrapperService
	) {
		// todo: update stats when new song is requested or something maybe idk what im thinking
		this.apiWrapper.getStats().subscribe({
			next: value => {
				const labels = value.requests_grouped_by_date.map((x) => {
					return x.date;
				});
				const data = value.requests_grouped_by_date.map((x) => x.request_count);


				let chartable_requests: ChartConfiguration["data"] = {
					xLabels: labels,

					yLabels: ["Request count"],

					datasets: [
						{
							data,
							label: "Request count"
						}
					]
				};

				this._currentStats.next({request_grouped_by_date_chartable: chartable_requests, ...value});
			}
		});
	}
}
