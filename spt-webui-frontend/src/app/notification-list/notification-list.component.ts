import { Component } from '@angular/core';
import { NotificationsService } from "../notifications.service";
import { AsyncPipe, JsonPipe, NgClass } from "@angular/common";

@Component({
  selector: 'app-notification-list',
  standalone: true,
	imports: [
		AsyncPipe,
		JsonPipe,
		NgClass
	],
  templateUrl: './notification-list.component.html',
  styleUrl: './notification-list.component.sass'
})
export class NotificationListComponent {

	constructor(
		protected notificationsService: NotificationsService,
	) {
	}
}
