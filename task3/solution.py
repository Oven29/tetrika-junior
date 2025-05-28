from typing import Dict, List, Tuple


def merge_intervals(intervals: List[int]) -> List[Tuple[int, int]]:
    pairs = sorted((intervals[i], intervals[i + 1]) for i in range(0, len(intervals), 2))
    merged = []

    for start, end in pairs:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))

    return merged


def crop_intervals(intervals: List[Tuple[int, int]], bounds: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Обрезаем интервалы рамками урока"""
    result = []
    for start, end in intervals:
        cropped_start = max(start, bounds[0])
        cropped_end = min(end, bounds[1])
        if cropped_start < cropped_end:
            result.append((cropped_start, cropped_end))

    return result


def intersect_intervals(a: List[Tuple[int, int]], b: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Находим пересечения интервалов a и b"""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        start_a, end_a = a[i]
        start_b, end_b = b[j]
        start = max(start_a, start_b)
        end = min(end_a, end_b)
        if start < end:
            result.append((start, end))
        if end_a < end_b:
            i += 1
        else:
            j += 1
    return result


def appearance(intervals: Dict[str, List[int]]) -> int:
    lesson_time = tuple(intervals["lesson"])
    pupil_intervals = merge_intervals(intervals["pupil"])
    tutor_intervals = merge_intervals(intervals["tutor"])

    pupil_in_lesson = crop_intervals(pupil_intervals, lesson_time)
    tutor_in_lesson = crop_intervals(tutor_intervals, lesson_time)

    overlap = intersect_intervals(pupil_in_lesson, tutor_in_lesson)

    return sum(end - start for start, end in overlap)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                       1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                       1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                       1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
    },
    {'intervals': {'lesson': [1594730400, 1594734000],
             'pupil': [1594730400, 1594734000],
             'tutor': [1594730400, 1594734000]},
     'answer': 3600
    },
]


def main():
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    print('All tests passed')


if __name__ == '__main__':
    main()
