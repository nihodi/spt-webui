import { Component, signal } from '@angular/core';
import {
	AbstractControl,
	FormBuilder,
	FormControl,
	FormGroup, ReactiveFormsModule,
	ValidationErrors,
	ValidatorFn,
	Validators
} from "@angular/forms";
import { SptWebUiApiWrapperService } from "../../api-services/spt-web-ui-api-wrapper.service";
import { PlaybackStateService } from "../../state-services/playback-state.service";
import { HttpErrorResponse } from "@angular/common/http";
import { TrackCardComponent } from "../../track-card/track-card.component";
import { AsyncPipe } from "@angular/common";
import { TrackListComponent } from "../../track-list/track-list.component";
import { AuthService } from "../../state-services/auth.service";
import { Subscription } from "rxjs";
import { NotificationsService } from "../../notifications.service";

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
		TrackListComponent
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
		private notificationsService: NotificationsService
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

	addToQueue($event: SubmitEvent) {
		const url = new URL(this.addToQueueForm.value.url!);
		url.search = "";

		this.addToQueueForm.disable();

		this.apiWrapper.addSongToQueue(url.toString()).subscribe({
			next: () => {
				setTimeout(() => {
					this.playbackState.updatePlaybackState();
				}, 10);

				this.addToQueueForm.reset();
				this.playbackState.addedSongToQueue();
				this.notificationsService.addNotification({
					type: "success",
					message: "Added song to queue!"
				});

			}, error: (err: HttpErrorResponse) => {
				this.addToQueueForm.enable();
				this.notificationsService.addNotification({
					type: "error",
					message: `Failed to request song. Code: ${err.status}`
				});
			}
		});
	}
}
