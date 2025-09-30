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

    mysql = {
      enable = lib.mkEnableOption "MySQL/MariaDB account and database creation";
    };

    nginx = {
      enable = lib.mkEnableOption "nginx integration";
    };

    settings = {

      # TODO: declare settings other than this
      # - port
      # everything else in the Environment class
      environmentFile = lib.mkOption {
        type = lib.types.path;
        description = "File to load as environment. Used to configure secret options.";
      };

      domain = lib.mkOption {
        type = lib.types.str;
        description = "Domain where the application is hosted";
      };

      baseHref = lib.mkOption {
        type = lib.types.nullOr lib.types.string;
        description = "Base path where the application is deployed";
        example = "/spt-webui";
        default = null;
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

    environment.etc."spt-webui/env" =
      let
        base = "https://${cfg.settings.domain}${cfg.settings.baseHref}";
      in
      {
        text = ''
          FRONTEND_URL=${base}
          ALLOWED_ORIGIN=${base}:80
          API_PREFIX=/api

          DISCORD_REDIRECT_URI=${base}/api/auth/callback/discord
          DISCORD_CLIENT_ID=${cfg.settings.discordClientId}

          SPOTIFY_REDIRECT_URI=${base}/api/auth/callback
          SPOTIFY_CLIENT_ID=${cfg.settings.spotify.clientId}
          SPOTIFY_ALLOWED_ACCOUNT_ID=${cfg.settings.spotify.allowedAccountId}
          TOKEN_SAVE_LOCATION=/var/spt-webui/saved_token

          ${lib.optionalString (
            cfg.settings.spotify.playlistId != null
          ) "SPOTIFY_PLAYLIST_ID=${cfg.settings.spotify.playlistId}"}

          ${lib.optionalString (cfg.mysql.enable) "DATABASE_URL=mariadb+pymysql:///spt_webui?unix_socket=/run/mysqld/mysqld.sock"}
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

    ## mariadb/mysql integration
    # create database and database user if it is enabled
    services.mysql = lib.mkIf cfg.mysql.enable {
      ensureUsers = [
        {
          name = "spt-webui-backend";
          ensurePermissions = {
            "spt_webui.*" = "ALL PRIVILEGES";
          };
        }
      ];

      ensureDatabases = [ "spt_webui" ];
    };

    ## nginx integration

    services.nginx =
      let
        spt-packages = inputs.self.packages.${pkgs.system};

        frontend-env = spt-packages.frontend-env {
          apiPrefix = "https://${cfg.settings.domain}${cfg.settings.baseHref}/api";
        };
        frontend = spt-packages.frontend { env = frontend-env; };
      in

      {
        virtualHosts.${cfg.settings.domain} = {
          locations."/${lib.stripPrefix "/" cfg.settings.baseHref}" = {
            root = "${frontend}";
            tryFiles = "\$uri /index.html";
          };

          locations."${if cfg.settings.baseHref != null then "/${lib.stripPrefix "/" cfg.settings.baseHref}/api" else "/api"}" = {
            proxyPass = "http://localhost:8000";
          };
        };
      };
  };
}
