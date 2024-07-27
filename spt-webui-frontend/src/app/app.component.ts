import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { JsonPipe } from "@angular/common";
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
	imports: [RouterOutlet, JsonPipe, ReactiveFormsModule],
	templateUrl: './app.component.html',
	styleUrl: './app.component.scss'
})
export class AppComponent {

	constructor(private fb: FormBuilder, private apiWrapper: SptWebUiApiWrapperService) {
		this.addToQueueForm = this.fb.group({
			url: ['', [Validators.required, matchesSpotifyUrl]]
		});
	}

	addToQueueForm: FormGroup<{url: FormControl<string | null>}>;

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
