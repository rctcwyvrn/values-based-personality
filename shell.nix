{
  pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/50ab793786d9de88ee30ec4e4c24fb4236fc2674.tar.gz";
    sha256 = "1s2gr5rcyqvpr58vxdcb095mdhblij9bfzaximrva2243aal3dgx";
  }) { },
}:

let
  python = pkgs.python3;
  pythonEnv = python.withPackages (ps: [
    ps.flask
    ps.gunicorn
    ps.pytest
  ]);
in
pkgs.mkShell {
  packages = [ pythonEnv ];

  shellHook = ''
    export FLASK_APP=app
  '';
}
