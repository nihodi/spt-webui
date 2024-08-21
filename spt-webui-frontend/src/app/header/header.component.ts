import { Component, signal } from '@angular/core';
import { AuthService } from "../state-services/auth.service";
import { Observable } from "rxjs";
import { UserData } from "../api-services/models";
import { AsyncPipe, JsonPipe, NgClass } from "@angular/common";
import { environment } from "../../environments/environment";
import { NotificationsService } from "../notifications.service";

@Component({
  selector: 'app-header',
  standalone: true,
	imports: [
		AsyncPipe,
		JsonPipe,
		NgClass
	],
  templateUrl: './header.component.html',
  styleUrl: './header.component.sass'
})
export class HeaderComponent {
	isLoadingUserData$: Observable<boolean>;
	isLoggedIn$: Observable<boolean>;
	currentUserData$: Observable<UserData | null>;

	protected environment = environment;

	popoverOpen = signal<boolean>(false);

	constructor(
		protected authService: AuthService,
		private notificationsService: NotificationsService
	) {
		this.isLoadingUserData$ = this.authService.isLoading$;
		this.currentUserData$ = this.authService.currentUserData$;
		this.isLoggedIn$ = this.authService.isLoggedIn$;
	}

	logOut() {
		this.popoverOpen.set(false);

		this.authService.logOut().subscribe({
			next: () => {
				this.notificationsService.addNotification({
					type: "info",
					message: "Logged out!"
				});
			}
		});
	}
}
