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
