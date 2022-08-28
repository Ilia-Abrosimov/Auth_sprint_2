import json


def film_for_person(person_id):
    query = {
        "query": {
            "bool": {
                "should": [
                    {"nested": {
                        "path": "writers",
                        "query": {
                            "bool": {
                                "must": [
                                    {"match": {"writers.id": str(person_id)}}
                                ]
                            }
                        }
                    }
                    },
                    {"nested": {
                        "path": "actors",
                        "query": {
                            "bool": {
                                "must": [
                                    {"match": {"actors.id": str(person_id)}}
                                ]
                            }
                        }
                    }
                    }]
            }
        }
    }
    return json.dumps(query)
