# returns a spt-webui-backend package based on inputs and a system
{
  nixpkgs,
  pyproject-nix,
  uv2nix,
  pyproject-build-systems,
  ...
}@inputs:
{ system }:

let
  inherit (nixpkgs) lib;

  workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ../..; };
  overlay = workspace.mkPyprojectOverlay {
    # overlay with the packages from uv.lock
    sourcePreference = "wheel";
  };

  python = pkgs.python313;
  pythonSet =
    (pkgs.callPackage pyproject-nix.build.packages {
      # i have no clue what this does
      inherit python;
    }).overrideScope
      (
        lib.composeManyExtensions [
          pyproject-build-systems.overlays.wheel
          overlay
        ]
      );

  pkgs = nixpkgs.legacyPackages.${system};
  inherit (pkgs.callPackages pyproject-nix.build.util { }) mkApplication;
in

mkApplication {
  venv = pythonSet.mkVirtualEnv "application-env" workspace.deps.default;
  package = pythonSet.spt-webui;
}
