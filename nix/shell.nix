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
  export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath buildInputs}

  make install
  '';
}