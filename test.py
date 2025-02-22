def can_generate_sequence(sequence, K):
    element_counts = {}
    first_occurrences = {}
    last_occurrences = {}
    unique_elements = set(sequence)

    # Single pass to gather necessary information
    for index, element in enumerate(sequence):
        element_counts[element] = element_counts.get(element, 0) + 1
        if element not in first_occurrences:
            first_occurrences[element] = index
        last_occurrences[element] = index

    unique_count = len(unique_elements)

    if unique_count > K:
        return False

    if K == 1:
        return unique_count == 1

    if K == 2:
        if unique_count == 1:
            return True
        elif unique_count == 2:
            # Using precomputed counts and occurrences to check conditions
            unique_elements = list(unique_elements)
            element1, element2 = unique_elements[0], unique_elements[1]
            if element_counts[element1] == first_occurrences[element2] or element_counts[element2] == first_occurrences[element1]:
                return True

            smallest_unit = find_smallest_repeat_unit(sequence, element_counts)
            if smallest_unit and smallest_unit != sequence:
                return is_unit_repeating(sequence, smallest_unit)
        return False

    if K == 3:
        if unique_count == 1:
            return True
        elif unique_count == 2:
            if check_dividing_strategy(sequence, 1, element_counts):
                return True
        elif unique_count == 3:
            if check_three_distinct_pattern(sequence, element_counts):
                return True

            smallest_unit = find_smallest_repeat_unit(sequence, element_counts)
            if smallest_unit and smallest_unit != sequence:
                return is_unit_repeating(sequence, smallest_unit)

            if check_three_number_dividing_strategy(sequence, element_counts):
                return True

    return False

def check_dividing_strategy(sequence, K_target, element_counts):
    for i in range(1, len(sequence)):
        part_a, part_b = sequence[:i], sequence[i:]
        if can_generate_sequence(part_a, K_target) or can_generate_sequence(part_b, K_target):
            return True
    return False

def check_three_number_dividing_strategy(sequence, element_counts):
    for i in range(1, len(sequence)):
        part_a, part_b = sequence[:i], sequence[i:]
        conditions_met = ((can_generate_sequence(part_a, 1) and can_generate_sequence(part_b, 2)) or
                          (can_generate_sequence(part_a, 2) and can_generate_sequence(part_b, 1)))
        if conditions_met:
            return True
    return False

def check_three_distinct_pattern(sequence, element_counts):
    if len(set(sequence)) != 3:
        return False

    first, second, third = sequence[0], None, None
    found_second, found_third = False, False

    for num in sequence[1:]:
        if not found_second:
            if num != first:
                second = num
                found_second = True
        elif not found_third:
            if num != first and num != second:
                third = num
                found_third = True
                break

    if not found_third:
        return False

    first_count = element_counts[first]
    second_count = element_counts[second]
    third_count = element_counts[third]

    expected_pattern = [first] * first_count + [second] * second_count + [third] * third_count
    return sequence == expected_pattern

def find_smallest_repeat_unit(sequence, element_counts):
    for unit_length in range(1, len(sequence) // 2 + 1):
        unit = sequence[:unit_length]
        if is_unit_repeating(sequence, unit):
            return unit
    return None

def is_unit_repeating(sequence, unit):
    unit_length = len(unit)
    for i in range(0, len(sequence), unit_length):
        if sequence[i:i+unit_length] != unit:
            return False
    return True

if __name__ == "__main__":
    T = int(input())
    results = []
    for _ in range(T):
        N, K =map(int, input().split())
        sequence = list(map(int, input().split()))
        # Instead of recomputing here, use the counts from within the main function
        result = can_generate_sequence(sequence, K)
        results.append("YES" if result else "NO")
    for result in results:
        print(result)
