{
  description = "Dev shell with Python server";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python3
          pkgs.lsof
          pkgs.imagemagick
          pkgs.ghostscript
          (pkgs.writeShellApplication {
            name = "serve";
            text = ''
              nohup python -m http.server 8008 > server.log 2>&1 &
              echo "Python web server started on http://localhost:8008 (logs in server.log)"
            '';
          })
          (pkgs.writeShellApplication {
            name = "stop";
            text = ''
              PID=$(lsof -ti:8008 2>/dev/null | head -1)
              if [ -n "$PID" ]; then
                kill "$PID" 2>/dev/null
                echo "Stopped server on port 8008 (PID: $PID)"
              else
                echo "No server running on port 8008"
              fi
              rm -f server.log
            '';
          })
        ];
      };
    };
}

