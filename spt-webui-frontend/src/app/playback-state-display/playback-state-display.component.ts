import { Component, input, InputSignal } from '@angular/core';
import { IconComponent } from "../icon/icon.component";
import { AsyncPipe } from "@angular/common";
import { millisecondsToTimeString, PlaybackState } from "../api-services/models";

@Component({
	selector: 'app-playback-state-display',
	standalone: true,
	imports: [
		IconComponent,
		AsyncPipe
	],
	templateUrl: './playback-state-display.component.html',
	styleUrl: './playback-state-display.component.sass'
})
export class PlaybackStateDisplayComponent {
	playbackState: InputSignal<PlaybackState> = input.required<PlaybackState>();
	protected readonly millisecondsToTimeString = millisecondsToTimeString;
}
