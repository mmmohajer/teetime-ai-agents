increment_version() {
  local version=$1
  local type=$2
  IFS='.' read -r major minor patch <<< "$version"

  case $type in
    major)
      major=$((major + 1))
      minor=0
      patch=0
      ;;
    minor)
      minor=$((minor + 1))
      patch=0
      ;;
    patch)
      patch=$((patch + 1))
      ;;
    none)
      echo "$version"
      return 0
      ;;
    *)
      echo "Invalid version increment type: $type"
      return 1
      ;;
  esac

  echo "$major.$minor.$patch"
}

prompt_for_version_bump() {
    local component=$1
    local bump
  
    bump=$(readData "What is the build for $component? (patch|minor|major|none)")
    if [[ "$bump" =~ ^(patch|minor|major|none)$ ]]; then
      echo "$bump"
      return 0
    else
      prompt_for_version_bump $component
    fi
  
}

update_constants_file() {
    local nginx_ver=$1
    local client_ver=$2
    local api_ver=$3
    cat << EOF > ./utils/shellScripting/constants/versioning.sh
NGINX_VERSION="$nginx_ver"
CLIENT_VERSION="$client_ver"
API_VERSION="$api_ver"
EOF
}