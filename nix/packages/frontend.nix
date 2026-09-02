{ pkgs, self, ... }:
{ env }:

pkgs.buildNpmPackage {
  pname = "spt-webui-frontend";
  version = "0.0.0";
  src = "${self}/spt-webui-frontend";

  postPatch = ''
    mkdir -p src/environments
    cp ${env} src/environments/environment.prod.ts
  '';

  installPhase = ''
    mkdir -p $out
    mv dist/spt-webui-frontend/browser/* $out/
  '';

  npmDepsHash = "sha256-AgVclvdq0d/flHT/fQ1ivKaNtfYgqbkFlu0Tmc87pBw=";
}
