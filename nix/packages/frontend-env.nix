{ pkgs, ... }:
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
}
