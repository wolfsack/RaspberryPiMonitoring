FROM grafana/grafana:8.2.1

ENV GF_USERS_ALLOW_SIGN_UP "true"

# Add provisioning
ADD ./provisioning /etc/grafana/provisioning
# Add configuration file
ADD ./grafana.ini /etc/grafana/grafana.ini
# Add dashboard json files
ADD ./dashboards /etc/grafana/dashboards