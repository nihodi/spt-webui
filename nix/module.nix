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
      environmentFiles = lib.mkOption {
        type = lib.types.listOf lib.types.path;
        description = "File to load as environment. Used to configure secret options.";
      };
    };
  };

  config = lib.mkIf cfg.enable {
    assertions =
      if cfg.enable then
        [
          {
            assertion = lib.hasAttr "environmentFiles" cfg.settings;
          }
        ]
      else
        [ ];

    # FIXME: MAKE UNPRIVILEGED spt-webui USER SO THE BACKEND DOES NOT RUN AS ROOT!!
    systemd.services.spt-webui = {
      description = "spt-webui backend";
      after = [ "network.target" ];

      serviceConfig = {
        ExecStart = "${inputs.self.packages.${system}.default}/bin/spt_webui_backend --env-files ${lib.concatStringsSep cfg.settings.environmentFiles "--env-files"}";
      };
      wantedBy = [ "multi-user.target" ];
    };
  };
}
