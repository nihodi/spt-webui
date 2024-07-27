import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../environments/environment";

@Injectable({
	providedIn: 'root'
})
export class SptWebUiApiWrapperService {

	constructor(
		private httpClient: HttpClient,
	) {
	}

	getPlaybackState(): Observable<any> {
		// any type is temporary
		return this.httpClient.get<any>(`${environment.api_prefix}/playback/state`);
	}

	getQueue(): Observable<any> {
		return this.httpClient.get<any>(`${environment.api_prefix}/playback/queue`);
	}
}
