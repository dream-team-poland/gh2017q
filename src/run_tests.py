from collections import defaultdict
import os
import functools

from root import PROJECT_DIR
from src.greedy_per_cache import greedy_per_cache
from src.greedy_request import greedy, priority_video_small, priority_video_big, min_latency
from src.common import write_output, read_input
from src.greedy_request import priority_count, best_fit
from src.score import count_score

TEST_FILENAMES = ['me_at_the_zoo.in', 'trending_today.in', 'videos_worth_spreading.in', 'kittens.in']
TEST_DATA_PATH = os.path.join(PROJECT_DIR, 'data')
TEST_RESULT_PATH = os.path.join(PROJECT_DIR, 'results')
TEST_FILE_PATHS = [os.path.join(TEST_DATA_PATH, filename) for filename in TEST_FILENAMES]

# (folder_name, test_function)
#
# test_function(input) -> output
#

TEST_CASES = [
    ('greedy_count_best_fit', functools.partial(greedy, priority_count, best_fit)),
    ('greedy_video_small_best_fit', functools.partial(greedy, priority_video_small, best_fit)),
    ('greedy_video_big_best_fit', functools.partial(greedy, priority_video_big, best_fit)),
    ('greedy_count_min_latency', functools.partial(greedy, priority_count, min_latency)),
    ('greedy_video_small_min_latency', functools.partial(greedy, priority_video_small, min_latency)),
    ('greedy_video_big_min_latency', functools.partial(greedy, priority_video_big, min_latency)),
    ('greedy_per_cache', greedy_per_cache)
]


def run_tests():
    max_for_file = defaultdict(int)
    output_for_max = {}
    for folder_name, test_function in TEST_CASES:
        folder_path = os.path.join(TEST_RESULT_PATH, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        total_score = 0
        print('Running test: {}'.format(test_function))
        for test_file_path in TEST_FILE_PATHS:
            print('Running file: {}'.format(test_file_path))
            with open(test_file_path) as test_file:
                input = read_input(test_file)
            output = test_function(input)
            output_file_path = os.path.join(
                folder_path,
                '{}_{}'.format(folder_name, os.path.basename(test_file_path))
            )
            with open(output_file_path, 'w') as output_file:
                write_output(output, output_file)
            file_score = count_score(input, output)
            if file_score > max_for_file[test_file_path]:
                max_for_file[test_file_path] = file_score
                output_for_max[test_file_path] = output_file_path
            print('Score for file: {}'.format(file_score))
            total_score += file_score
        print('Total score: {}'.format(total_score))
    print('Max_for_file: {}'.format(max_for_file))
    print('Max score: {}'.format(sum(max_for_file.values())))
    print('Output for max: {}'.format(output_for_max))


if __name__ == '__main__':
    run_tests()
