{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-24.11") {} }:
pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python312.withPackages (ps: [
      ps.openai-whisper
      ps.ffmpeg-python
    ]))
  ];
  shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/:$LD_LIBRARY_PATH
  '';
}
  
