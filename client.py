def filter_own_position(client_id, positions_data):
    filtered = {key: value for key, value in positions_data.items() if key != client_id}
    return filtered

positions_data = {
    'd3bfad6d-c2da-456a-89f5-608d927312d9': {'x': 0.0, 'y': 6.814326763153076, 'z': 0.0}
}
your_client_id = 'd3bfad6d-c2da-456a-89f5-608d927312d9'

filtered_positions = filter_own_position(your_client_id, positions_data)

print(filtered_positions)