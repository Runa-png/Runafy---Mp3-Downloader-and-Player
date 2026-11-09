
{
  description = "Runafy NixOS runtime compatibility";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      runafyEnv = pkgs.buildFHSEnv {
        name = "runafy";

        targetPkgs = pkgs: with pkgs; [
          libGL
          glib
          zlib
          stdenv.cc.cc.lib
          xorg.libX11
          xorg.libXext
          xorg.libXrender
          xorg.libXfixes
          xorg.libXrandr
          xorg.libxcb
          ffmpeg
          pipewire
          alsa-lib
          qt6.qtbase
          qt6.qtmultimedia
        ];

        runScript = "bash";
      };
    in
    {
      packages.${system}.default = runafyEnv;

      apps.${system}.default = {
        type = "app";
        program = "${runafyEnv}/bin/runafy";
      };
    };
}
