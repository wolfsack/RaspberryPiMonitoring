FROM grafana/grafana:6.5.0

ENV GF_USERS_ALLOW_SIGN_UP=true

# Add provisioning
ADD ./provisioning /etc/grafana/provisioning/
# Add configuration file
ADD ./grafana.ini /etc/grafana/grafana.ini
# Add dashboard json files
ADD ./dashboards /etc/grafana/dashboards