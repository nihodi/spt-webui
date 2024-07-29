import { Component, input } from '@angular/core';
import { TrackObject } from "../api-services/models";

@Component({
	selector: 'app-track-list',
	standalone: true,
	imports: [],
	templateUrl: './track-list.component.html',
	styleUrl: './track-list.component.sass'
})
export class TrackListComponent {
	tracks = input.required<TrackObject[]>();
	protected readonly Math = Math;

	protected millisecondsToTimeString(ms: number): string {
		const minutes = Math.floor(ms  / 60000);
		const seconds = Math.floor((ms % 60000) / 1000);

		if (seconds < 10)
			return `${minutes}:0${seconds}`;
		else
			return `${minutes}:${seconds}`;
	}
}
