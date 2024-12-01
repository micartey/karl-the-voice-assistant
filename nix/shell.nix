{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell rec {
  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    portaudio
  ];

  shellHook = ''
  make install
  '';
}