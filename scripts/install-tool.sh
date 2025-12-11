#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <tool> <version>"
  echo "Supported tools: uv gh git rg fd jq yq just"
  exit 1
fi

TOOL="$1"
REQUESTED_VERSION="$2"

# Trim leading "v" from requested version when comparing / building filenames,
# but preserve it where needed for tag names.
strip_v() {
  local v="$1"
  echo "${v#v}"
}

# Compare deb-style versions using dpkg if available
# Returns 0 if v1 >= v2, 1 otherwise
version_ge() {
  local v1="$1"
  local v2="$2"
  if ! command -v dpkg >/dev/null 2>&1; then
    # Fallback: simple equality check only
    [[ "$v1" == "$v2" ]]
    return
  fi
  dpkg --compare-versions "$v1" ge "$v2"
}

get_current_version_simple() {
  # Expect "<name> X.Y.Z" → extract 2nd field
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo ""
    return
  fi
  "$cmd" --version 2>/dev/null | head -n1 | awk '{print $2}'
}

install_uv() {
  local version="$1"
  local plain_version
  plain_version="$(strip_v "$version")"

  local current
  current="$(get_current_version_simple uv)"

  if [[ -n "$current" && "$current" == "$plain_version" ]]; then
    echo "uv $plain_version already installed. Nothing to do."
    return
  fi

  echo "Installing uv $plain_version…"
  # astral.sh installer supports --version
  curl -LsSf https://astral.sh/uv/install.sh \
    | UV_INSTALL_VERSION="$plain_version" sh

  echo "uv installed:"
  uv --version
}

install_gh() {
  local version="$1"
  local plain_version
  plain_version="$(strip_v "$version")"

  local current
  current="$(get_current_version_simple gh)"

  if [[ -n "$current" && "$current" == "$plain_version" ]]; then
    echo "gh $plain_version already installed. Nothing to do."
    return
  fi

  echo "Installing gh $plain_version…"

  local tmpdir
  tmpdir="$(mktemp -d)"
  local deb="${tmpdir}/gh.deb"
  local tag="v${plain_version}"

  wget "https://github.com/cli/cli/releases/download/${tag}/gh_${plain_version}_linux_amd64.deb" \
    -O "$deb"

  sudo dpkg -i "$deb" || sudo apt-get -y -f install

  rm -rf "$tmpdir"

  echo "gh installed:"
  gh --version | head -n1
}

install_fd() {
  local version="$1"
  local plain_version
  plain_version="$(strip_v "$version")"
  local tag="v${plain_version}"

  local current
  current="$(get_current_version_simple fd)"

  if [[ -n "$current" && "$current" == "$plain_version" ]]; then
    echo "fd $plain_version already installed. Nothing to do."
    return
  fi

  echo "Installing fd $plain_version…"

  local tmpdir
  tmpdir="$(mktemp -d)"
  local archive="${tmpdir}/fd.tar.gz"
  local tarball="fd-${tag}-x86_64-unknown-linux-musl.tar.gz"

  wget "https://github.com/sharkdp/fd/releases/download/${tag}/${tarball}" \
    -O "$archive"

  tar -xzf "$archive" -C "$tmpdir"

  sudo install -m 755 \
    "${tmpdir}/fd-${tag}-x86_64-unknown-linux-musl/fd" \
    /usr/local/bin/fd

  rm -rf "$tmpdir"

  echo "fd installed:"
  fd --version
}

install_yq() {
  local version="$1"
  local plain_version
  plain_version="$(strip_v "$version")"
  local tag="v${plain_version}"

  local current
  current="$(get_current_version_simple yq)"

  if [[ -n "$current" && "$current" == "$plain_version" ]]; then
    echo "yq $plain_version already installed. Nothing to do."
    return
  fi

  echo "Installing yq $plain_version…"

  sudo wget "https://github.com/mikefarah/yq/releases/download/${tag}/yq_linux_amd64" \
    -O /usr/local/bin/yq
  sudo chmod +x /usr/local/bin/yq

  echo "yq installed:"
  yq --version
}

install_just() {
  local version="$1"
  local plain_version="${version#v}"

  # Get current version if installed
  local current
  current=$(just --version 2>/dev/null | awk '{print $2}' || true)

  if [[ "$current" == "$plain_version" ]]; then
    echo "just $plain_version already installed. Nothing to do."
    return
  fi

  echo "Installing just $plain_version…"

  local tmpdir
  tmpdir="$(mktemp -d)"
  local filename="just-${plain_version}-x86_64-unknown-linux-musl.tar.gz"
  local archive="${tmpdir}/${filename}"

  # Download archive
  wget "https://github.com/casey/just/releases/download/${plain_version}/${filename}" \
    -O "$archive"

  # Extract
  tar -xzf "$archive" -C "$tmpdir"

  # Locate the `just` binary (layout-safe)
  local bin
  bin="$(find "$tmpdir" -maxdepth 3 -type f -name just | head -n 1)"

  if [[ -z "$bin" ]]; then
    echo "ERROR: Could not find 'just' binary inside the archive."
    echo "       Check the release assets or update the installer."
    rm -rf "$tmpdir"
    exit 1
  fi

  echo "Installing to /usr/local/bin/just (requires sudo)…"
  sudo install -m 755 "$bin" /usr/local/bin/just

  rm -rf "$tmpdir"

  echo -n "just installed: "
  just --version
}



install_git() {
  local min_version="$1"

  if command -v git >/dev/null 2>&1; then
    local current
    current="$(git --version 2>/dev/null | awk '{print $3}')"
    if version_ge "$current" "$min_version"; then
      echo "git $current >= $min_version already installed. Nothing to do."
      return
    else
      echo "git $current < $min_version, updating via apt…"
    fi
  else
    echo "git not installed, installing via apt…"
  fi

  sudo apt-get update
  sudo apt-get install -y git

  echo "git installed:"
  git --version
}

install_rg() {
  local min_version="$1"

  if command -v rg >/dev/null 2>&1; then
    local current
    current="$(rg --version 2>/dev/null | head -n1 | awk '{print $2}')"
    if version_ge "$current" "$min_version"; then
      echo "ripgrep $current >= $min_version already installed. Nothing to do."
      return
    else
      echo "ripgrep $current < $min_version, updating via apt…"
    fi
  else
    echo "ripgrep not installed, installing via apt…"
  fi

  sudo apt-get update
  sudo apt-get install -y ripgrep

  echo "ripgrep installed:"
  rg --version | head -n1
}

install_jq() {
  local min_version="$1"

  if command -v jq >/dev/null 2>&1; then
    local current
    current="$(jq --version 2>/dev/null | sed 's/^jq-//')"
    if version_ge "$current" "$min_version"; then
      echo "jq $current >= $min_version already installed. Nothing to do."
      return
    else
      echo "jq $current < $min_version, updating via apt…"
    fi
  else
    echo "jq not installed, installing via apt…"
  fi

  sudo apt-get update
  sudo apt-get install -y jq

  echo "jq installed:"
  jq --version
}

case "$TOOL" in
  uv)
    install_uv "$REQUESTED_VERSION"
    ;;
  gh)
    install_gh "$REQUESTED_VERSION"
    ;;
  fd)
    install_fd "$REQUESTED_VERSION"
    ;;
  yq)
    install_yq "$REQUESTED_VERSION"
    ;;
  just)
    install_just "$REQUESTED_VERSION"
    ;;
  git)
    install_git "$REQUESTED_VERSION"
    ;;
  rg)
    install_rg "$REQUESTED_VERSION"
    ;;
  jq)
    install_jq "$REQUESTED_VERSION"
    ;;
  *)
    echo "ERROR: Unsupported tool: $TOOL"
    echo "Supported tools: uv gh git rg fd jq yq just"
    exit 1
    ;;
esac
