def detect_relationships(claims):

    lines = claims.split("\n")

    relationships = []

    for i in range(len(lines)-1):

        relation = {
            "source": lines[i],
            "target": lines[i+1],
            "type": "related"
        }

        relationships.append(relation)

    return relationships