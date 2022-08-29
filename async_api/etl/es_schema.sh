curl -XPUT http://${ELASTICSEARCH__HOST}:${ELASTICSEARCH__PORT}/movies -H 'Content-Type: application/json' -d @./movies.json
curl -XPUT http://${ELASTICSEARCH__HOST}:${ELASTICSEARCH__PORT}/genres -H 'Content-Type: application/json' -d @./genres.json
curl -XPUT http://${ELASTICSEARCH__HOST}:${ELASTICSEARCH__PORT}/persons -H 'Content-Type: application/json' -d @./persons.json