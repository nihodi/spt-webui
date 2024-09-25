import { Component } from '@angular/core';
import {
	AbstractControl,
	FormBuilder,
	FormControl,
	FormGroup,
	ReactiveFormsModule,
	ValidationErrors,
	ValidatorFn,
	Validators
} from "@angular/forms";
import { SptWebUiApiWrapperService } from "../../api-services/spt-web-ui-api-wrapper.service";
import { PlaybackStateService } from "../../state-services/playback-state.service";
import { HttpErrorResponse } from "@angular/common/http";
import { TrackCardComponent } from "../../track-card/track-card.component";
import { AsyncPipe, JsonPipe } from "@angular/common";
import { TrackListComponent } from "../../track-list/track-list.component";
import { AuthService } from "../../state-services/auth.service";
import { Subscription } from "rxjs";
import { NotificationsService } from "../../notifications.service";
import { PlaybackStateDisplayComponent } from "../../playback-state-display/playback-state-display.component";
import { SpinnerComponent } from "../../spinner/spinner.component";
import { StatsStateService } from "../../api-services/stats-state.service";
import { RollingCounterComponent } from "../../rolling-counter/rolling-counter.component";
import { BaseChartDirective } from "ng2-charts";
import { AppPopularTracksListComponent } from "../../app-popular-tracks-list/app-popular-tracks-list.component";

const matchesSpotifyUrl: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
	const regex = /https:\/\/open.spotify.com\/track\/[a-zA-Z0-9]+/g;

	if (regex.test(control.value))
		return null;

	return {
		"spotifyUrl": "Does not match a valid spotify URL!"
	};
}


@Component({
	selector: 'app-index',
	standalone: true,
	imports: [
		TrackCardComponent,
		AsyncPipe,
		ReactiveFormsModule,
		TrackListComponent,
		PlaybackStateDisplayComponent,
		SpinnerComponent,
		JsonPipe,
		RollingCounterComponent,
		BaseChartDirective,
		AppPopularTracksListComponent
	],
	templateUrl: './index.component.html',
	styleUrl: './index.component.sass'
})
export class IndexComponent {
	constructor(
		private fb: FormBuilder,
		private apiWrapper: SptWebUiApiWrapperService,
		protected playbackState: PlaybackStateService,
		protected authService: AuthService,
		private notificationsService: NotificationsService,
		protected statsService: StatsStateService
	) {
		this.addToQueueForm = this.fb.group({
			url: ['', [Validators.required, matchesSpotifyUrl]]
		});

		this.rateLimitTimerSubscription = this.playbackState.rateLimitCountdown$.subscribe({
			next: value => {
				if (value !== null)
					this.addToQueueForm.disable();
				else
					this.addToQueueForm.enable();
			}
		});
	}

	rateLimitTimerSubscription: Subscription;

	addToQueueForm: FormGroup<{ url: FormControl<string | null> }>;

	addToQueue() {
		const url = new URL(this.addToQueueForm.value.url!);
		url.search = "";

		this.addToQueueForm.disable();

		this.apiWrapper.addSongToQueue(url.toString()).subscribe({
			next: (track) => {
				setTimeout(() => {
					this.playbackState.updatePlaybackState();
				}, 10);

				this.addToQueueForm.reset();
				this.playbackState.addedSongToQueue();
				this.notificationsService.addNotification({
					type: "success",
					message: `Added ${ track.name } by ${ track.artists.map(x => x.name).join(", ") } to the queue!`
				});

			}, error: (err: HttpErrorResponse) => {
				this.addToQueueForm.enable();

				if (err.status === 409) {
					this.notificationsService.addNotification({
						type: "error",
						message: `Failed to request song. Reason: Song is already in the queue or is already playing!`
					});

					return;
				}

				this.notificationsService.addNotification({
					type: "error",
					message: `Failed to request song. Code: ${ err.status }`
				});
			}
		});
	}

	msToDaysHoursMinutes = (value: number): string => {
		const days = Math.floor(value / (60 * 60 * 24 * 1000));
		const hours = Math.floor((value - (days * 60 * 60 * 24 * 1000)) / (60 * 60 * 1000));
		const minutes = Math.floor((value - (hours * 60 * 60 * 1000) - (days * 60 * 60 * 24 * 1000)) / (60 * 1000));

		return `${days}d ${hours}h ${minutes}m`;
	}
}
