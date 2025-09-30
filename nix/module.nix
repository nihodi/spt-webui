inputs:
{
  config,
  lib,
  pkgs,
  ...
}:

let

  cfg = config.services.spt-webui;
  inherit (pkgs.stdenv.hostPlatform) system;
in
{

  options.services.spt-webui = {
    enable = lib.mkEnableOption "spt-webui-backend";

    settings = {

      # TODO: declare settings other than this
      # - port
      # everything else in the Environment class
      environmentFile = lib.mkOption {
        type = lib.types.path;
        description = "File to load as environment. Used to configure secret options.";
      };

      baseHref = lib.mkOption {
        type = lib.types.string;
        description = "Base path where the application is deployed";
        example = "https://dodooc.dietzel.no/";
      };

      spotify = {
        allowedAccountId = lib.mkOption {
          type = lib.types.string;
          description = "Account ID of the Spotify account that should be controlled from spt-webui";
        };

        clientId = lib.mkOption {
          type = lib.types.string;
          description = "Spotify OAuth2 client id. The client secret is set using the `environmentFile`.";
        };

        playlistId = lib.mkOption {
          type = lib.types.nullOr lib.types.string;
          default = null;
          description = "Spotify playlist all requested songs get added to.";
        };
      };

      discordClientId = lib.mkOption {
        type = lib.types.string;
        description = "Discord OAuth2 client id. The client secret is set using the `environmentFile`";
      };
    };
  };

  config = lib.mkIf cfg.enable {
    assertions =
      if cfg.enable then
        [

        ]
      else
        [ ];

    systemd.services.spt-webui = {
      description = "spt-webui backend";
      after = [ "network.target" ];

      serviceConfig = {
        User = "spt-webui-backend";
        Group = "spt-webui-backend";

        ExecStart = "${
          inputs.self.packages.${system}.default
        }/bin/spt_webui_backend --env-file ${cfg.settings.environmentFile} --env-file /etc/spt-webui/env";
      };
      wantedBy = [ "multi-user.target" ];
    };

    environment.etc."spt-webui/env" = {
      text = ''
        FRONTEND_URL=${cfg.settings.baseHref}
        ALLOWED_ORIGIN=${cfg.settings.baseHref}:80
        API_PREFIX=/api

        DISCORD_REDIRECT_URI=${cfg.settings.baseHref}api/auth/callback/discord

        SPOTIFY_REDIRECT_URI=${cfg.settings.baseHref}api/auth/callback
        SPOTIFY_CLIENT_ID=${cfg.settings.spotify.clientId}
        SPOTIFY_ALLOWED_ACCOUNT_ID=${cfg.settings.spotify.allowedAccountId}
        TOKEN_SAVE_LOCATION=/var/spt-webui/saved_token

        ${lib.optionalString cfg.settings.spotify.playlistId != null "SPOTIFY_PLAYLIST_ID=${cfg.settings.spotify.playlistId}"}
      '';
      user = "spt-webui-backend";
      group = "spt-webui-backend";
      mode = "0440";
    };

    systemd.tmpfiles.rules = [
      "f /var/spt-webui/saved_token 0770 spt-webui-backend spt-webui-backend -"
    ];

    users.users.spt-webui-backend = {
      isSystemUser = true;
      group = "spt-webui-backend";
    };

    users.groups.spt-webui-backend = {
    };
  };
}
