let
  nixpkgs = builtins.fetchGit {
    name = "nixos-unstable-2021-03-17";
    url = "https://github.com/nixos/nixpkgs/";
    ref = "refs/heads/nixos-unstable";
    rev = "266dc8c3d052f549826ba246d06787a219533b8f";
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs nixos-unstable`
  };
  pkgs = import nixpkgs { config = {}; };

  opencvGtk = opencv: opencv.override (old : { enableGtk2 = true; });
  pythonPkgs = python-packages: with python-packages; [
      ptpython # used for dev
      pytest # testing
      (opencvGtk opencv3)
      face_recognition
      pyserial
    ];
  pythonCore = pkgs.python38;
  myPython = pythonCore.withPackages pythonPkgs;
in
pkgs.mkShell {
  buildInputs =
  with pkgs;
  [
    minicom
    git
    gnumake
    myPython
    wget
    arduino-cli
  ];
}
