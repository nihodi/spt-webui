import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AsyncPipe, JsonPipe } from "@angular/common";
import {
	AbstractControl,
	FormBuilder,
	FormControl,
	FormGroup,
	ReactiveFormsModule, ValidationErrors,
	ValidatorFn,
	Validators
} from "@angular/forms";
import { SptWebUiApiWrapperService } from "./api-services/spt-web-ui-api-wrapper.service";
import { PlaybackStateService } from "./state-services/playback-state.service";
import { TrackCardComponent } from "./track-card/track-card.component";
import { TrackListComponent } from "./track-list/track-list.component";

const matchesSpotifyUrl: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
	const regex = /https:\/\/open.spotify.com\/track\/[a-zA-Z0-9]+/g;

	if (regex.test(control.value))
		return null;

	return {
		"spotifyUrl": "Does not match a valid spotify URL!"
	};
}


@Component({
	selector: 'app-root',
	standalone: true,
	imports: [RouterOutlet, JsonPipe, ReactiveFormsModule, AsyncPipe, TrackCardComponent, TrackListComponent],
	templateUrl: './app.component.html',
	styleUrl: './app.component.scss'
})
export class AppComponent {

	constructor(
		private fb: FormBuilder,
		private apiWrapper: SptWebUiApiWrapperService,
		protected playbackState: PlaybackStateService
		) {
		this.addToQueueForm = this.fb.group({
			url: ['', [Validators.required, matchesSpotifyUrl]]
		});
	}

	addToQueueForm: FormGroup<{ url: FormControl<string | null> }>;

	addToQueue($event: SubmitEvent) {
		const url = new URL(this.addToQueueForm.value.url!);
		url.search = "";

		this.apiWrapper.addSongToQueue(url.toString()).subscribe({
			next: value => {
				console.log("epic");
			}
		})
	}
}
