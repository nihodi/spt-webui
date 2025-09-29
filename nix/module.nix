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
    };
  };

  config = lib.mkIf cfg.enable {
    assertions =
      if cfg.enable then
        [

        ]
      else
        [ ];

    # FIXME: MAKE UNPRIVILEGED spt-webui USER SO THE BACKEND DOES NOT RUN AS ROOT!!
    systemd.services.spt-webui = {
      description = "spt-webui backend";
      after = [ "network.target" ];

      serviceConfig = {
        User = "spt-webui-backend";
        Group = "spt-webui-backend";

        ExecStart = "${
          inputs.self.packages.${system}.default
        }/bin/spt_webui_backend --env-file ${cfg.settings.environmentFile}";
      };
      wantedBy = [ "multi-user.target" ];
    };

    users.users.spt-webui-backend = {
      isSystemUser = true;
      group = "spt-webui-backend";
    };

    users.groups.spt-webui-backend = {

    };
  };
}
