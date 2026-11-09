
{
  description = "PyQt6 multimedia development shell";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      python = pkgs.python313.withPackages (ps: [
        ps.pyqt6
        ps.mutagen
        ps.yt-dlp
        ps.fuzzywuzzy
        ps.pyinstaller
      ]);

      qtPlugins = pkgs.symlinkJoin {
        name = "qt-plugins";
        paths = [
          pkgs.qt6.qtbase
          pkgs.qt6.qtmultimedia
        ];
      };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          python
          pkgs.qt6.qtbase
          pkgs.qt6.qtmultimedia
          pkgs.pipewire
          pkgs.wireplumber
          pkgs.ffmpeg
        ];

        shellHook = ''
          export QT_PLUGIN_PATH="${qtPlugins}/lib/qt-6/plugins"
          export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt6.qtbase}/lib/qt-6/plugins/platforms"

          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
            pkgs.pipewire
            pkgs.wireplumber
            pkgs.ffmpeg
          ]}:''${LD_LIBRARY_PATH:-}"
        '';
      };
    };
}

