import { Component } from '@angular/core';
import { AuthService } from "../state-services/auth.service";
import { Observable } from "rxjs";
import { UserData } from "../api-services/models";
import { AsyncPipe, JsonPipe } from "@angular/common";
import {environment} from "../../environments/environment";

@Component({
  selector: 'app-header',
  standalone: true,
	imports: [
		AsyncPipe,
		JsonPipe
	],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
	isLoadingUserData$: Observable<boolean>;
	isLoggedIn$: Observable<boolean>;
	currentUserData$: Observable<UserData | null>;

	protected environment = environment;

	constructor(
		private authService: AuthService,
	) {
		this.isLoadingUserData$ = this.authService.isLoading$;
		this.currentUserData$ = this.authService.currentUserData$;
		this.isLoggedIn$ = this.authService.isLoggedIn$;
	}

	logOut() {
		this.authService.logOut().subscribe({
			next: () => {

			}
		});
	}
}
