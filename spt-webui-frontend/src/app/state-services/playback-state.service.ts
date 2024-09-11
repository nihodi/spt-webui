import { Injectable } from '@angular/core';
import { SptWebUiApiWrapperService } from "../api-services/spt-web-ui-api-wrapper.service";
import { BehaviorSubject, interval, map, retry, Subscription } from "rxjs";
import { PlaybackState, SpotifyQueue } from "../api-services/models";
import { HttpErrorResponse } from "@angular/common/http";
import { NotificationsService } from "../notifications.service";

@Injectable({
	providedIn: 'root'
})
export class PlaybackStateService {

	private _playbackState: BehaviorSubject<PlaybackState | null> = new BehaviorSubject<PlaybackState | null>(null);
	playbackState$ = this._playbackState.asObservable();

	private _spotifyQueue: BehaviorSubject<SpotifyQueue | null> = new BehaviorSubject<SpotifyQueue | null>(null);
	queue$ = this._spotifyQueue.asObservable();

	isPlaying$ = this._playbackState.pipe(map(v => v !== null));

	private rateLimitCountDownSource: BehaviorSubject<number | null> = new BehaviorSubject<number | null>(null);
	private decreaseSecondsLeftSubscription: Subscription | null = null;

	rateLimitCountdown$ = this.rateLimitCountDownSource.asObservable();

	private isUpdatingState: null | number = null;
	private incrementProjectedSongProgressTimer: null | number = null;

	private _isInitialLoad: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(true);
	isInitialLoad$ = this._isInitialLoad.asObservable();

	getPlaybackState(): PlaybackState | null {
		return this._playbackState.getValue();
	}

	getQueue(): SpotifyQueue | null {
		return this._spotifyQueue.getValue();
	}

	constructor(
		private apiWrapper: SptWebUiApiWrapperService,
		private notificationsService: NotificationsService
	) {
		this.updatePlaybackState();
	}

	updatePlaybackState() {
		console.log("updating playback state.");

		if (this.isUpdatingState)
			clearTimeout(this.isUpdatingState);

		if (this.incrementProjectedSongProgressTimer)
			clearInterval(this.incrementProjectedSongProgressTimer);


		this.apiWrapper.getPlaybackState().pipe(retry({delay: 1000, count: 1})).subscribe({
			next: state => {
				this._isInitialLoad.next(false);
				this._playbackState.next(state);

				this.isUpdatingState = null;
				this.schedulePlaybackStateUpdate();

				if (state?.is_playing) {
					this.incrementProjectedSongProgressTimer = setInterval(() => {
						this.incrementProjectedSongProgress();
					}, 1000);
				}
			},
			error: (err: HttpErrorResponse) => {
				this.schedulePlaybackStateUpdate();

				this.notificationsService.addNotification({
					type: "error",
					message: `Failed to fetch playback state. Trying again in 15 seconds.`,
				});
			}
		});

		this.apiWrapper.getQueue().pipe(retry({delay: 1000, count: 1})).subscribe({
			next: state => {
				this._spotifyQueue.next(state);
			}
		});
	}

	private incrementProjectedSongProgress(): void {
		let state = this.getPlaybackState();
		if (state === null)
			return;

		state.progress_ms += 1000;
		// clamp value to song length
		state.progress_ms = Math.min(state.item.duration_ms, state.progress_ms);

		this._playbackState.next(state);
	}

	private schedulePlaybackStateUpdate(): void {
		if (this.isUpdatingState)
			return;

		const state = this.getPlaybackState();
		let timeUntilSongEnds = null;
		if (state !== null) {
			timeUntilSongEnds = state?.item.duration_ms - state?.progress_ms;
		}

		this.isUpdatingState = setTimeout(() => {
			this.updatePlaybackState();
		}, Math.min(15_000, timeUntilSongEnds ?? 15_000));
	}

	addedSongToQueue(): void {
		const now = Date.now();
		this.rateLimitCountDownSource.next(60);

		this.decreaseSecondsLeftSubscription = interval(1000).subscribe({
			next: state => {
				this.rateLimitCountDownSource.next((this.rateLimitCountDownSource.getValue() ?? 60) - 1);

				if (state === 59) {
					this.decreaseSecondsLeftSubscription?.unsubscribe()
					this.decreaseSecondsLeftSubscription = null;
					this.rateLimitCountDownSource.next(null);
				}

			}
		});
	}
}
