import { Injectable } from '@angular/core';
import { BehaviorSubject } from "rxjs";


export interface Notification {
	type: "error" | "success" | "info";
	message: string;
}


@Injectable({
	providedIn: 'root'
})
export class NotificationsService {
	private currentNotificationsSource: BehaviorSubject<Notification[]> = new BehaviorSubject<Notification[]>([]);
	currentNotifications$ = this.currentNotificationsSource.asObservable();

	constructor() {
	}

	getCurrentNotifications(): Notification[] {
		return this.currentNotificationsSource.getValue();
	}

	addNotification(notification: Notification) {
		let current = this.getCurrentNotifications();
		current.push(notification);
		this.currentNotificationsSource.next(current);

		setTimeout(() => {
			let current = this.getCurrentNotifications();
			current.splice(0, 1);
			this.currentNotificationsSource.next(current);
		}, 10_000)
	}
}
