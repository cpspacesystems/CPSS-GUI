brew services start grafana \n brew services stop grafana

conda activate CPSS-GUI

docker run -d --name=grafana -p 3000:3000 grafana/grafana-oss
docker pull influxdb:2.2.0

grafana
    username: admin
    password: admin

influxdb
    username: admin
    password: password