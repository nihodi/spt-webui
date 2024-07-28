import { Component, input } from '@angular/core';
import { TrackObject } from "../api-services/models";

@Component({
	selector: 'app-track-card',
	standalone: true,
	imports: [],
	templateUrl: './track-card.component.html',
	styleUrl: './track-card.component.scss'
})
export class TrackCardComponent {
	track = input.required<TrackObject>();
}
