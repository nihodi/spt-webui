import { Component, computed, input, Signal } from '@angular/core';
import { CommonSong, DbSong, millisecondsToTimeString, toCommonSong, TrackObject } from "../api-services/models";


@Component({
	selector: 'app-track-list',
	standalone: true,
	imports: [
	],
	templateUrl: './track-list.component.html',
	styleUrl: './track-list.component.sass'
})
export class TrackListComponent {
	inputTracks = input.required<TrackObject[] | DbSong[]>({alias: "tracks"});

	tracks: Signal<CommonSong[]> = computed(() => {
		const input = this.inputTracks();
		return input.map(x => toCommonSong(x));
	});

	protected readonly millisecondsToTimeString = millisecondsToTimeString;
}
