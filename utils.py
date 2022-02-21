def build_sequence(points):
    # Build sequence linesans and save
    sequences = {}
    points_sorted = sorted(points, key=lambda item: int(item["properties"]["captured_at"]))
    for point in points_sorted:
        sequence_id = str(point["properties"]["sequence_id"])
        if sequence_id not in sequences.keys():
            sequences[sequence_id] = {
                "type": "Feature",
                "properties": {"sequence_id": sequence_id},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [point["geometry"]["coordinates"]],
                },
            }
        else:
            sequences[sequence_id]["geometry"]["coordinates"].append(
                point["geometry"]["coordinates"]
            )

    return list(sequences.values())
