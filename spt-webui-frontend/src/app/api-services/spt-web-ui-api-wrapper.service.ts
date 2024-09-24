import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../environments/environment";
import { ApiStats, PlaybackState, SpotifyQueue, TrackObject } from "./models";

@Injectable({
	providedIn: 'root'
})
export class SptWebUiApiWrapperService {

	constructor(
		private httpClient: HttpClient,
	) {
	}

	getPlaybackState(): Observable<PlaybackState | null> {
		// any type is temporary
		return this.httpClient.get<PlaybackState | null>(`${environment.api_prefix}/playback/state`);
	}

	getQueue(): Observable<SpotifyQueue> {
		return this.httpClient.get<SpotifyQueue>(`${environment.api_prefix}/playback/queue`);
	}

	addSongToQueue(url: string): Observable<TrackObject> {
		return this.httpClient.post<TrackObject>(`${environment.api_prefix}/playback/queue`, "", {
			params: {
				url
			}
		});
	}

	getStats(): Observable<ApiStats> {
		return this.httpClient.get<ApiStats>(`${environment.api_prefix}/stats`);
	}
}
