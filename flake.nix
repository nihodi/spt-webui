{
  description = "Develop Python on Nix with uv";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{
      nixpkgs,
      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
      self,
      ...
    }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
      overlay = workspace.mkPyprojectOverlay {
        # overlay with the packages from uv.lock
        sourcePreference = "wheel";
      };

      pythonSets = forAllSystems (
        # creates a pythonSet for each system
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python313;
        in
        (pkgs.callPackage pyproject-nix.build.packages {
          # i have no clue what this does
          inherit python;
        }).overrideScope
          (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.wheel
              overlay
            ]
          )
      );

    in
    {
      nixosModules.spt-webui = import ./nix/module.nix inputs;

      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            packages = [
              pkgs.python3
              pkgs.uv
            ];

            shellHook = ''
              unset PYTHONPATH
              uv sync
              . .venv/bin/activate
            '';
          };
        }
      );

      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          pythonSet = pythonSets.${system};
          inherit (pkgs.callPackages pyproject-nix.build.util { }) mkApplication;

        in
        {
          default = mkApplication {
            venv = pythonSet.mkVirtualEnv "application-env" workspace.deps.default;
            package = pythonSet.spt-webui;
          };

          frontend-env =
            {
              apiPrefix,
              baseHref ? null,
            }:
            pkgs.writeTextFile {
              name = "environment.prod.ts";
              text = ''
                export interface Environment {
                  api_prefix: string;
                  base_href?: string;
                }

                export const environment: Environment = {
                  api_prefix: "${apiPrefix}",
                  base_href: ${if baseHref == null then "undefined" else ''"${baseHref}"''}
                }
              '';
            };

          frontend =
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

              npmDepsHash = "sha256-wtBSP87okYx/nwo1EMImo2oF7c4lDnDE+0Z/i+GXG5U=";
            };
        }
      );
    };
}
