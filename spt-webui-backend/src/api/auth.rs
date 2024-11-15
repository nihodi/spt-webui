use poem::web::Data;
use poem_openapi::{ApiResponse, OpenApi};
use crate::SptWebuiSettings;

pub(crate) struct AuthApi;


#[derive(ApiResponse)]
enum AuthRedirectResponse {
    #[oai(status = 307)]
    Ok(#[oai(header = "Location")] String),
}


#[OpenApi(prefix_path = "/auth")]
impl AuthApi {
    #[oai(path = "/setup/discord", method = "get")]
    async fn hello(
		&self,
		settings: Data<&SptWebuiSettings>

	) -> AuthRedirectResponse {
        AuthRedirectResponse::Ok(
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
}
