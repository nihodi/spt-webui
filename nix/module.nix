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
    environment.systemPackages = [inputs.self.packages.${system}.default];
  };
}
