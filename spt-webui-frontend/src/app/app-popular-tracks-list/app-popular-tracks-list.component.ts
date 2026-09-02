import { Component, input, ChangeDetectionStrategy } from '@angular/core';
import { DbSong, millisecondsToTimeString, toCommonSong } from "../api-services/models";

@Component({
    selector: 'app-app-popular-tracks-list',
    imports: [],
    templateUrl: './app-popular-tracks-list.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './app-popular-tracks-list.component.sass'
})
export class AppPopularTracksListComponent {
	tracks = input.required<{
		song: DbSong;
		request_count: number;
	}[]>();

	protected readonly toCommonSong = toCommonSong;
	protected readonly millisecondsToTimeString = millisecondsToTimeString;
}
