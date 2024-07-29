import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from "@angular/common/http";
import { authInterceptor } from "./auth.interceptor";
import { APP_BASE_HREF } from "@angular/common";
import { environment } from "../environments/environment";

export const appConfig: ApplicationConfig = {
	providers: [
		{
			provide: APP_BASE_HREF,
			useValue: environment.base_href ?? "/"
		},
		provideZoneChangeDetection({eventCoalescing: true}),
		provideRouter(routes),
		provideHttpClient(
			withInterceptors([
				authInterceptor
			])
		)]
};
