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

  assertions = if cfg.enable then [
    {
      assertion = false;
      message = "test assertion :)";
    }

  ] else [];

  options.services.spt-webui = {
    enable = lib.mkEnableOption "spt-webui-backend";
  };

  config = lib.mkIf cfg.enable {
    # FIXME: MAKE UNPRIVILEGED spt-webui USER SO THE BACKEND DOES NOT RUN AS ROOT!!
    systemd.services.spt-webui = {
      description = "spt-webui backend";
      after = [ "network.target" ];

      script = "${inputs.self.packages.${system}.default}/bin/spt_webui_backend";
      wantedBy = [ "multi-user.target" ];
    };
  };
}
