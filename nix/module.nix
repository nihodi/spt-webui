inputs:
{ config, lib, pkgs, ... }:

let

  cfg = config.services.spt-webui;
  inherit (pkgs.stdenv.hostPlatform) system;
in
{

  options.services.spt-webui = {
    enable = lib.mkEnableOption "spt-webui-backend";
  };

  config = lib.mkIf cfg.enable {
    systemd.services.spt-webui = {
      description = "spt-webui backend";
      after = "network.target";

      script = "${inputs.self.packages.${system}.default}/bin/spt_webui_backend";
      wantedBy = "multi-user.target";
    };
  };
}
