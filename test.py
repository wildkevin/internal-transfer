def toggle_coordinate_value(canvas, coord):
    x, y = coord
    # Toggle the value at the given coordinate
    canvas[x][y] = 1 - canvas[x][y]

def get_reflected_coordinates(coord, N):
    x, y = coord
    return [(x, y), (x, N - y - 1), (N - x - 1, y), (N - x - 1, N - y - 1)]

def get_group_value(canvas, coord, N):
    values = []
    reflected_coords = get_reflected_coordinates(coord, N)
    for r_coord in reflected_coords:
        x, y = r_coord
        value = canvas[x][y]
        values.append(value)
    occur_one = sum(values)
    occur_zero = 4 - occur_one
    return min(occur_one, occur_zero)

def generate_canvas(grid, N):
    canvas = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if grid[i][j] == '#':
                canvas[i][j] = 1
    return canvas

def toggle_and_update_group_value(canvas, coord, N, groups):
    toggle_coordinate_value(canvas, coord)
    reflected_coords = tuple(sorted(get_reflected_coordinates(coord, N)))
    group_value = get_group_value(canvas, coord, N)
    # Update the group's value and the total group value
    old_value = groups.get(reflected_coords)
    groups[reflected_coords] = group_value
    return group_value - old_value

if __name__ == "__main__":
    N, U = map(int, input().split())
    grid = [input() for _ in range(N)]
    canvas = generate_canvas(grid, N)

    groups = {}
    total_group_value = 0
    for i in range(N):
        for j in range(N):
            group_id = tuple(sorted(get_reflected_coordinates((i, j), N)))
            if group_id not in groups:
                group_value = get_group_value(canvas, (i, j), N)
                groups[group_id] = group_value
                total_group_value += group_value

    print(total_group_value)  # Initial sum of group values

    for _ in range(U):
        x, y = map(int, input().split())
        coord = (x - 1, y - 1)  # Adjust for 0-indexing
        change_in_value = toggle_and_update_group_value(canvas, coord, N, groups)
        total_group_value += change_in_value
        print(total_group_value)  # Updated sum of group values after each update


def max_occurrences_or_missing(numbers, max_value):
    # Count occurrences of each number in the input list
    occurrence_counts = {}
    for num in numbers:
        occurrence_counts[num] = occurrence_counts.get(num, 0) + 1

    # Calculate the cumulative count of missing numbers
    missing_counts = [0] * (max_value + 1)
    for i in range(1, max_value + 1):
        missing_counts[i] = missing_counts[i - 1] + (0 if i in occurrence_counts else 1)

    # Determine the max between occurrences and missing counts for each number
    results = []
    for x in range(max_value + 1):
        occurrences_of_x = occurrence_counts.get(x, 0)
        missing_up_to_x = missing_counts[x - 1] if x > 0 else 0
        results.append(max(occurrences_of_x, missing_up_to_x))

    return results


if __name__ == "__main__":
    N = int(input().strip())
    num_list = list(map(int, input().strip().split()))
    results = max_occurrences_or_missing(num_list, N)
    for result in results:
        print(result)
