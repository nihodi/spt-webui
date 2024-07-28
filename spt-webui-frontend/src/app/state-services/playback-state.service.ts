import { Injectable } from '@angular/core';
import { SptWebUiApiWrapperService } from "../api-services/spt-web-ui-api-wrapper.service";
import { BehaviorSubject } from "rxjs";
import { PlaybackState, SpotifyQueue } from "../api-services/models";

@Injectable({
	providedIn: 'root'
})
export class PlaybackStateService {

	private _playbackState: BehaviorSubject<PlaybackState | null> = new BehaviorSubject<PlaybackState | null>(null);
	playbackState$ = this._playbackState.asObservable();

	private _spotifyQueue: BehaviorSubject<SpotifyQueue | null> = new BehaviorSubject<SpotifyQueue | null>(null);
	queue$ = this._spotifyQueue.asObservable();

	private isUpdatingState: null | number = null;

	getPlaybackState(): PlaybackState | null {
		return this._playbackState.getValue();
	}

	getQueue(): SpotifyQueue | null {
		return this._spotifyQueue.getValue();
	}

	constructor(
		private apiWrapper: SptWebUiApiWrapperService
	) {
		this.updatePlaybackState();
	}

	updatePlaybackState() {
		if (this.isUpdatingState)
			clearTimeout(this.isUpdatingState);

		console.log("updating playback state.");

		this.apiWrapper.getPlaybackState().subscribe({
			next: state => {
				this._playbackState.next(state);

				this.isUpdatingState = null;
				this.schedulePlaybackStateUpdate();
			}
		});

		this.apiWrapper.getQueue().subscribe({
			next: state => {
				this._spotifyQueue.next(state);
			}
		});
	}

	private schedulePlaybackStateUpdate(): void {
		if (this.isUpdatingState)
			return;

		// TODO: more logic to update "smarter"

		const state = this.getPlaybackState();
		this.isUpdatingState = setTimeout(() => {
			this.updatePlaybackState();
		}, 15_000);
	}
}
