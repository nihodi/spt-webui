import { Component, computed, input, ChangeDetectionStrategy } from '@angular/core';
import { TrackObject } from "../api-services/models";

@Component({
    selector: 'app-track-card',
    imports: [],
    templateUrl: './track-card.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './track-card.component.scss'
})
export class TrackCardComponent {
	track = input.required<TrackObject>();
}
