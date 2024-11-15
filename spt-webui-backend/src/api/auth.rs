use std::convert::Into;
use std::fmt::format;
use poem::web::Data;
use poem_openapi::{auth::Bearer, ApiResponse, OAuthScopes, OpenApi, SecurityScheme};
use poem_openapi::param::Query;
use poem_openapi::payload::PlainText;
use crate::SptWebuiSettings;

pub(crate) struct AuthApi;


#[derive(ApiResponse)]
enum AuthRedirectResponse {
	/// Redirect to Discord OAuth
	#[oai(status = 307)]
	DiscordOk(
		/// URL to Discord OAuth
		/// `https://discord.com/oauth2/authorize`
		#[oai(header = "Location")] String
	),
}

#[derive(ApiResponse)]
enum OAuth2CallbackResponse {
	#[oai(status = 307)]
	Response(
		/// URL to frontend with parameters indicating what happened
		#[oai(header = "Location")] String
	),
}

#[OpenApi(prefix_path = "/auth")]
impl AuthApi {
	#[oai(path = "/setup/discord", method = "get")]
	async fn discord_redirect(
		&self,
		settings: Data<&SptWebuiSettings>,
	) -> AuthRedirectResponse {
		AuthRedirectResponse::DiscordOk(
			url::Url::parse_with_params(
				"https://discord.com/oauth2/authorize",
				[
					("client_id", &settings.discord_client_id.to_string()),
					("response_type", &"code".to_string()),
					("redirect_uri", &settings.discord_redirect_uri),
					("scope", &"identify".to_string()),
					("prompt", &"none".to_string()),
				],
			).unwrap().into(),
		)
	}


	#[oai(path = "/callback/discord", method = "get")]
	async fn discord_callback(
		&self,
		Query(code): Query<Option<String>>,
		Query(err): Query<Option<String>>,

		settings: Data<&SptWebuiSettings>,
	) -> OAuth2CallbackResponse {
		match code {
			Some(code) => {
				// do discord stuff
				OAuth2CallbackResponse::Response(
					url::Url::parse_with_params(
						settings.frontend_url.as_str(),
						[
							("auth_success", "1"),
						],
					).unwrap().into()
				)
			},
			None => {
				OAuth2CallbackResponse::Response(
					url::Url::parse_with_params(
						settings.frontend_url.as_str(),
						[
							("auth_err", &err.unwrap().to_string()),
						],
					).unwrap().into(),
				)
			}
		}
	}
}
