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
		if (this.isUpdatingState)
			clearTimeout(this.isUpdatingState);

		console.log("updating playback state.");

		this.apiWrapper.getPlaybackState().pipe(retry({delay: 1000, count: 1})).subscribe({
			next: state => {
				this._playbackState.next(state);

				this.isUpdatingState = null;
				this.schedulePlaybackStateUpdate();
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

	private schedulePlaybackStateUpdate(): void {
		if (this.isUpdatingState)
			return;

		// TODO: more logic to update "smarter"

		const state = this.getPlaybackState();
		this.isUpdatingState = setTimeout(() => {
			this.updatePlaybackState();
		}, 15_000);
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
