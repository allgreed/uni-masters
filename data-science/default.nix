let
  nixpkgs = builtins.fetchGit {
    name = "nixos-unstable-2021-01-9";
    url = "https://github.com/nixos/nixpkgs-channels/";
    ref = "refs/heads/nixos-unstable";
    rev = "84d74ae9c9cbed73274b8e4e00be14688ffc93fe";
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
  };
  pkgs = import nixpkgs { config = {}; };
  pythonCore = pkgs.python38;
  # TODO: how to link this to pythonCore version? o.0
  pyeasyga = with pkgs.python38Packages; buildPythonPackage rec {
      pname = "pyeasyga";
      version = "0.3.1";

      src = fetchPypi{
        inherit version;
        inherit pname;
        sha256 = "049zm9lddzvv0001wyqxg38cbiqizzh5009rvxbp82v5bpz1vkhi";
      };

      # tests are not stateless - they make a HTTP call :c
      doCheck = false;

      buildInputs = [ six ];
  };
  chesspy = with pkgs.python38Packages; buildPythonPackage rec {
      pname = "chess";
      version = "1.3.3";

      src = fetchPypi{
        inherit version;
        inherit pname;
        sha256 = "1hha9vggsgy0a4r1h7wwymxadsm9r5j66vw0wa6zhhzjvwhh34i7";
      };

      doCheck = false;
  };
  apyori = with pkgs.python38Packages; buildPythonPackage rec {
      pname = "apyori";
      version = "1.1.2";

      src = fetchPypi{
        inherit version;
        inherit pname;
        sha256 = "1v32siqfg5ljgpmmh13v711q4lxch4xzi33068a1navk2k7zzrp2";
      };

      doCheck = false;
  };
  pythonPkgs = python-packages: with python-packages; [
      pytest
      chesspy
      numpy
      matplotlib
      pandas
      pyeasyga
      pydantic
      deap
      scikitlearn
      pytorch
      apyori
    ]; 
  myPython = pythonCore.withPackages pythonPkgs;
in
pkgs.mkShell {
  buildInputs =
  with pkgs;
  [
    myPython
    git
    gnumake
    stockfish
  ];
}
