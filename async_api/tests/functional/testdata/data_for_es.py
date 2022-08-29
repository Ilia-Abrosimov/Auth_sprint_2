import json

films = [{
    "id": "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
    "title": "Star Wars: Episode IV - A New Hope",
    "description": ("The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage in their "
                    "efforts to quell the rebellion against the Galactic Empire. Luke Skywalker and Han Solo, captain"
                    " of the Millennium Falcon, work together with the companionable droid duo R2-D2 and C-3PO to "
                    "rescue the beautiful princess, help the Rebel Alliance and restore freedom and justice to the "
                    "Galaxy."),
    "actors": [
        {
            "id": "26e83050-29ef-4163-a99d-b546cac208f8",
            "name": "Mark Hamill"
        },
        {
            "id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",
            "name": "Harrison Ford"
        },
        {
            "id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358",
            "name": "Carrie Fisher"
        },
        {
            "id": "e039eedf-4daf-452a-bf92-a0085c68e156",
            "name": "Peter Cushing"
        }
    ],
    "actors_names": [
        "Mark Hamill",
        "Harrison Ford",
        "Carrie Fisher",
        "Peter Cushing"
    ],
    "director": [
        "George Lucas"
    ],
    "genre": [
        "Adventure",
        "Action",
        "Sci-Fi",
        "Fantasy"
    ],
    "imdb_rating": 8.6,
    "writers": [
        {
            "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
            "name": "George Lucas"
        }
    ],
    "writers_names": [
        "George Lucas"
    ]
},
    {
        "id": "025c58cd-1b7e-43be-9ffb-8571a613579b",
        "title": "Star Wars: Episode VI - Return of the Jedi",
        "description": ("Luke Skywalker battles horrible Jabba the Hut and cruel Darth Vader to save his comrades in"
                        " the Rebel Alliance and triumph over the Galactic Empire. Han Solo and Princess Leia reaffirm"
                        " their love and team with Chewbacca, Lando Calrissian, the Ewoks and the androids C-3PO and"
                        " R2-D2 to aid in the disruption of the Dark Side and the defeat of the evil emperor."),
        "actors": [
            {
                "id": "26e83050-29ef-4163-a99d-b546cac208f8",
                "name": "Mark Hamill"
            },
            {
                "id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",
                "name": "Harrison Ford"
            },
            {
                "id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358",
                "name": "Carrie Fisher"
            },
            {
                "id": "efdd1787-8871-4aa9-b1d7-f68e55b913ed",
                "name": "Billy Dee Williams"
            }
        ],
        "actors_names": [
            "Mark Hamill",
            "Harrison Ford",
            "Carrie Fisher",
            "Billy Dee Williams"
        ],
        "director": [
            "Richard Marquand"
        ],
        "genre": [
            "Adventure",
            "Action",
            "Sci-Fi",
            "Fantasy"
        ],
        "imdb_rating": 8.3,
        "writers": [
            {
                "id": "3217bc91-bcfc-44eb-a609-82d228115c50",
                "name": "Lawrence Kasdan"
            },
            {
                "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
                "name": "George Lucas"
            }
        ],
        "writers_names": [
            "Lawrence Kasdan",
            "George Lucas"
        ]
    }
]

persons = [{
    "id": "26e83050-29ef-4163-a99d-b546cac208f8",
    "name": "Mark Hamill",
    "role": [
        "actor",
        "director"
    ],
    "film_ids": [
        "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
        "025c58cd-1b7e-43be-9ffb-8571a613579b"
    ]
},
    {
        "id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",
        "name": "Harrison Ford",
        "role": [
            "actor"
        ],
        "film_ids": [
            "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
            "025c58cd-1b7e-43be-9ffb-8571a613579b"
        ]
    },
    {
        "id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358",
        "name": "Carrie Fisher",
        "role": [
            "actor"
        ],
        "film_ids": [
            "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
            "025c58cd-1b7e-43be-9ffb-8571a613579b"
        ]
    },
    {
        "id": "e039eedf-4daf-452a-bf92-a0085c68e156",
        "name": "Peter Cushing",
        "role": [
            "actor"
        ],
        "film_ids": [
            "3d825f60-9fff-4dfe-b294-1a45fa1e115d"
        ]
    },
    {
        "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
        "name": "George Lucas",
        "role": [
            "actor",
            "director",
            "writer"
        ],
        "film_ids": [
            "3d825f60-9fff-4dfe-b294-1a45fa1e115d",
            "025c58cd-1b7e-43be-9ffb-8571a613579b"
        ]
    },
    {
        "id": "efdd1787-8871-4aa9-b1d7-f68e55b913ed",
        "name": "Billy Dee Williams",
        "role": [
            "actor"
        ],
        "film_ids": [
            "025c58cd-1b7e-43be-9ffb-8571a613579b"
        ]
    },
    {
        "id": "3217bc91-bcfc-44eb-a609-82d228115c50",
        "name": "Lawrence Kasdan",
        "role": [
            "actor",
            "writer"
        ],
        "film_ids": [
            "025c58cd-1b7e-43be-9ffb-8571a613579b"
        ]
    }
]

genres = [{
    "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
    "name": "Adventure",
    "description": None,
},
    {
        "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
        "name": "Action",
        "description": None,
    },
    {
        "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
        "name": "Sci-Fi",
        "description": None,
    },
    {
        "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
        "name": "Fantasy",
        "description": None,
    }
]


def data_for_elastic():
    json_list = []
    for item in films:
        index_info = {"index": {"_index": "movies", "_id": item["id"]}}
        json_list.append(index_info)
        json_list.append(item)
    for item in persons:
        index_info = {"index": {"_index": "persons", "_id": item["id"]}}
        json_list.append(index_info)
        json_list.append(item)
    for item in genres:
        index_info = {"index": {"_index": "genres", "_id": item["id"]}}
        json_list.append(index_info)
        json_list.append(item)
    dumps_list = [json.dumps(dct) for dct in json_list]
    json_list = "\n".join(dumps_list)
    json_list += "\n"
    return json_list
