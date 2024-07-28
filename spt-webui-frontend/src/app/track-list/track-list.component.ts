import { Component, input } from '@angular/core';
import { TrackObject } from "../api-services/models";

@Component({
  selector: 'app-track-list',
  standalone: true,
  imports: [],
  templateUrl: './track-list.component.html',
  styleUrl: './track-list.component.scss'
})
export class TrackListComponent {
	tracks = input.required<TrackObject[]>();
}
