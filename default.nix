with import <nixpkgs> {};
with pkgs.python37Packages;

let
  pythonPackages = python-packages: with python-packages; [
    ipython
    jupyterlab
    scrapy
    virtualenvwrapper
    black
  ];
  python3WithPackages = pkgs.python37.withPackages pythonPackages;
in
stdenv.mkDerivation {
  name = "course-explorer";
  buildInputs = [
    python3WithPackages
  ];
}
