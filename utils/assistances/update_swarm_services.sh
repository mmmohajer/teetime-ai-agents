for service in $(docker stack services app --format '{{.Name}}'); do
  docker service update --force "$service";
done
