deployInLocal() {
  local nginxBump=$(prompt_for_version_bump "nginx")
  local clientBump=$(prompt_for_version_bump "client")
  local apiBump=$(prompt_for_version_bump "API")
  local janusBump=$(prompt_for_version_bump "Janus")

  buildClient $clientBump

  local nginx_ver=$(increment_version "$NGINX_VERSION" "$nginxBump")
  local client_ver=$(increment_version "$CLIENT_VERSION" "$clientBump")
  local api_ver=$(increment_version "$API_VERSION" "$apiBump")
  local janus_ver=$(increment_version "$JANUS_VERSION" "$janusBump")

  update_constants_file "$nginx_ver" "$client_ver" "$api_ver" "$janus_ver"

local script=$( cat << EOF
export NGINX_REPO=$NGINX_REPO
export CLIENT_REPO=$CLIENT_REPO
export API_REPO=$API_REPO
export JANUS_REPO=$JANUS_REPO
export NGINX_VERSION=$nginx_ver
export CLIENT_VERSION=$client_ver
export API_VERSION=$api_ver
export JANUS_VERSION=$janus_ver
export CELERY_FLOWER_USER=$CELERY_FLOWER_USER
export CELERY_FLOWER_PASSWORD=$CELERY_FLOWER_PASSWORD
[ -f "docker-swarm.tmp.yml" ] && rm docker-swarm.tmp.yml
envsubst < docker-compose-swarm.yml > docker-compose-swarm-tmp.yml
docker build -t \$NGINX_REPO:\$NGINX_VERSION -f nginx/Dockerfile ./nginx && docker build -t \$CLIENT_REPO:\$CLIENT_VERSION -f client/Dockerfile ./client && docker build -t \$API_REPO:\$API_VERSION -f api/Dockerfile ./api && docker build -t \$JANUS_REPO:\$JANUS_VERSION -f janus/Dockerfile ./janus && docker push \$NGINX_REPO:\$NGINX_VERSION && docker push \$CLIENT_REPO:\$CLIENT_VERSION && docker push \$API_REPO:\$API_VERSION && docker push \$JANUS_REPO:\$JANUS_VERSION && docker stack deploy -c docker-compose-swarm-tmp.yml app --with-registry-auth
EOF
)
bash -c "$script" 
}

deployToProdWithSwarm() {
  local nginxBump=$(prompt_for_version_bump "nginx")
  local clientBump=$(prompt_for_version_bump "client")
  local apiBump=$(prompt_for_version_bump "API")
  local janusBump=$(prompt_for_version_bump "Janus")

  buildClient $clientBump

  local nginx_ver=$(increment_version "$NGINX_VERSION" "$nginxBump")
  local client_ver=$(increment_version "$CLIENT_VERSION" "$clientBump")
  local api_ver=$(increment_version "$API_VERSION" "$apiBump")
  local janus_ver=$(increment_version "$JANUS_VERSION" "$janusBump")

  update_constants_file "$nginx_ver" "$client_ver" "$api_ver" "$janus_ver"

  local commitMsg="Ready for new release to production server: $(date)"
  git add .
  git commit -m "$commitMsg"
  git push origin master

local script=$( cat << EOF
cd /var/www/app;
git pull origin master;
export NGINX_REPO=$NGINX_REPO
export CLIENT_REPO=$CLIENT_REPO
export API_REPO=$API_REPO
export JANUS_REPO=$JANUS_REPO
export NGINX_VERSION=$nginx_ver
export CLIENT_VERSION=$client_ver
export API_VERSION=$api_ver
export JANUS_VERSION=$janus_ver
export CELERY_FLOWER_USER=$CELERY_FLOWER_USER
export CELERY_FLOWER_PASSWORD=$CELERY_FLOWER_PASSWORD
export COTURN_REALM=$COTURN_REALM
export COTURN_USER=$COTURN_USER
export COTURN_PASSWORD=$COTURN_PASSWORD
export COTURN_EXTERNAL_IP=$COTURN_EXTERNAL_IP
[ -f "docker-swarm.tmp.yml" ] && rm docker-swarm.tmp.yml
envsubst < docker-compose-swarm.yml > docker-compose-swarm-tmp.yml
docker build -t \$NGINX_REPO:\$NGINX_VERSION -f nginx/Dockerfile ./nginx && docker build -t \$CLIENT_REPO:\$CLIENT_VERSION -f client/Dockerfile ./client && docker build -t \$API_REPO:\$API_VERSION -f api/Dockerfile ./api && docker build -t \$JANUS_REPO:\$JANUS_VERSION -f janus/Dockerfile ./janus && docker push \$NGINX_REPO:\$NGINX_VERSION && docker push \$CLIENT_REPO:\$CLIENT_VERSION && docker push \$API_REPO:\$API_VERSION && docker push \$JANUS_REPO:\$JANUS_VERSION && docker stack deploy -c docker-compose-swarm-tmp.yml app --with-registry-auth
EOF
)
ssh $PROD_SERVER_ALIAS "$script" 
}


deployToProdWithCompose() {
  local nginxBump=$(prompt_for_version_bump "nginx")
  local clientBump=$(prompt_for_version_bump "client")
  local apiBump=$(prompt_for_version_bump "API")

  buildClient $clientBump

  local nginx_ver=$(increment_version "$NGINX_VERSION" "$nginxBump")
  local client_ver=$(increment_version "$CLIENT_VERSION" "$clientBump")
  local api_ver=$(increment_version "$API_VERSION" "$apiBump")

  update_constants_file "$nginx_ver" "$client_ver" "$api_ver"

  local commitMsg="Ready for new release to production server: $(date)"
  git add .
  git commit -m "$commitMsg"
  git push origin master

local script=$( cat << EOF
cd /var/www/app;
git pull origin master;
docker compose -f docker-compose-prod.yml build && docker compose -f docker-compose-prod.yml up -d && docker volume prune -f && docker builder prune -a -f && docker image prune -a -f && docker container prune -f && docker network prune -f
EOF
)
ssh $PROD_SERVER_ALIAS "$script" 
}