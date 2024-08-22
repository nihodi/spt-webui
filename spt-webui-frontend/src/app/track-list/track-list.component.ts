import { Component, input } from '@angular/core';
import { millisecondsToTimeString, TrackObject } from "../api-services/models";




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

	protected readonly millisecondsToTimeString = millisecondsToTimeString;
}
