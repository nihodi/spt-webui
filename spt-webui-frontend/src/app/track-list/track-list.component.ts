import { Component, computed, input } from '@angular/core';
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

	// pretty artist strings for each of the TrackObjects in tracks.
	// e.g. ["Rudy Raw, Phlocalyst, Viktor Minsky", "morningtime, Blue Wednesday"]
	artists = computed(() => {
		let artists: string[] = [];

		for (const track of this.tracks()) {
			artists.push(track.artists.map(x => x.name).join(", "));
		}

		return artists;
	});

	protected readonly Math = Math;

	protected readonly millisecondsToTimeString = millisecondsToTimeString;
}
