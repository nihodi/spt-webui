{
  description = "Develop Python on Nix with uv";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
    in
    {
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
        in
        {
          default = pkgs.python313Packages.buildPythonPackage {
            pname = "spt_webui_backend";
            version = "0.0.1";
            pyproject = true;
            src = lib.fileset.toSource {
              root = ./.;
              fileset = lib.fileset.unions [ # only include needed files aka. exclude frontend files
                ./pyproject.toml
                ./uv.lock
                ./spt_webui_backend
              ];
            };

            build-system = with pkgs.python313Packages; [
              setuptools
              setuptools-scm
            ];

            dependencies = with pkgs.python313Packages; [
              alembic
              fastapi
              itsdangerous
              pydantic-settings
              pymysql
              requests-oauthlib
              sentry-sdk
              sqlalchemy
              uvicorn
            ];
          };
        }
      );
    };
}
