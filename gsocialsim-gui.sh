#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo ""
    echo "Shutting down..."
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null && echo "  Frontend stopped"
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null && echo "  Backend stopped"
    wait 2>/dev/null
    echo "Done."
}
trap cleanup EXIT INT TERM

# ---------- Flags ----------
BUILD_CPP=false
INSTALL_DEPS=false
BACKEND_PORT=8000
FRONTEND_PORT=5173

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Start the gsocialsim GUI (backend + frontend).

Options:
  --build        Rebuild the C++ binary before starting
  --install      Install Python + npm dependencies before starting
  --port PORT    Backend port (default: 8000)
  --ui-port PORT Frontend port (default: 5173)
  -h, --help     Show this help message
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --build)   BUILD_CPP=true; shift ;;
        --install) INSTALL_DEPS=true; shift ;;
        --port)    BACKEND_PORT="$2"; shift 2 ;;
        --ui-port) FRONTEND_PORT="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

# ---------- C++ build ----------
if $BUILD_CPP; then
    echo "==> Building C++ binary..."
    cmake -S "$ROOT/cpp" -B "$ROOT/cpp/build" -DCMAKE_BUILD_TYPE=Release
    cmake --build "$ROOT/cpp/build" -j"$(nproc)"
    echo ""
fi

CPP_BIN="$ROOT/cpp/build/gsocialsim_cpp"
if [ ! -f "$CPP_BIN" ]; then
    echo "C++ binary not found at $CPP_BIN"
    echo "Run with --build to compile, or build manually:"
    echo "  cmake -S cpp -B cpp/build && cmake --build cpp/build"
    exit 1
fi

# ---------- Python venv ----------
VENV="$ROOT/.gsocialsim"
if [ ! -d "$VENV" ]; then
    VENV="$ROOT/.venv"
fi
if [ -f "$VENV/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "$VENV/bin/activate"
else
    echo "No Python venv found at .gsocialsim/ or .venv/"
    echo "Create one: python3 -m venv .gsocialsim && source .gsocialsim/bin/activate"
    exit 1
fi

# ---------- Install deps ----------
if $INSTALL_DEPS; then
    echo "==> Installing Python dependencies..."
    pip install -q -r "$ROOT/gui/backend/requirements.txt"
    echo "==> Installing npm dependencies..."
    (cd "$ROOT/gui/frontend" && npm install --silent)
    echo ""
fi

# ---------- Check deps ----------
python -c "import fastapi" 2>/dev/null || {
    echo "Python dependencies not installed. Run with --install or:"
    echo "  pip install -r gui/backend/requirements.txt"
    exit 1
}

if [ ! -d "$ROOT/gui/frontend/node_modules" ]; then
    echo "Frontend dependencies not installed. Run with --install or:"
    echo "  cd gui/frontend && npm install"
    exit 1
fi

# ---------- Start backend ----------
echo "==> Starting backend on port $BACKEND_PORT..."
GSOCIALSIM_CPP_BINARY="$CPP_BIN" \
    uvicorn gui.backend.app.main:app \
    --host 0.0.0.0 --port "$BACKEND_PORT" \
    --log-level info &
BACKEND_PID=$!

# Wait for backend to be ready
echo -n "    Waiting for backend"
for i in $(seq 1 30); do
    if curl -sf "http://localhost:$BACKEND_PORT/api/health" >/dev/null 2>&1; then
        echo " ready!"
        break
    fi
    echo -n "."
    sleep 1
    if [ "$i" -eq 30 ]; then
        echo " TIMEOUT"
        echo "Backend failed to start. Check logs above."
        exit 1
    fi
done

# ---------- Start frontend ----------
echo "==> Starting frontend on port $FRONTEND_PORT..."
(cd "$ROOT/gui/frontend" && \
    VITE_BACKEND_PORT="$BACKEND_PORT" \
    npx vite --host 0.0.0.0 --port "$FRONTEND_PORT") &
FRONTEND_PID=$!

sleep 2

echo ""
echo "================================================"
echo "  gsocialsim GUI is running"
echo "  Frontend:  http://localhost:$FRONTEND_PORT"
echo "  Backend:   http://localhost:$BACKEND_PORT"
echo "  API docs:  http://localhost:$BACKEND_PORT/docs"
echo "  Press Ctrl+C to stop"
echo "================================================"
echo ""

wait
