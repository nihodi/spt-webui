self:
{ config, lib, pkgs }:

let

  cfg = config.options.services.spt-webui;
  inherit (pkgs.stdenv.hostPlatform) system;
in
{

  options.services.spt-webui = {
    enable = lib.mkEnableOption "spt-webui-backend";
  };

  config = lib.mkIf cfg.enable {
    environment.systemPackages = [self.packages.${system}.default];
  };
}
