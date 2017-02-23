import os

import functools

from root import PROJECT_DIR
from src.greedy_request import greedy, priority_video_small, priority_video_big
from src.common import write_output, read_input
from src.greedy_request import priority_count, best_fit
from src.score import count_score

TEST_FILENAMES = ['kittens.in', 'me_at_the_zoo.in', 'trending_today.in', 'videos_worth_spreading.in']
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
]


def run_tests():
    for folder_name, test_function in TEST_CASES:
        os.mkdir(folder_name)
        total_score = 0
        print('Running test: {}'.format(test_function))
        for test_file_path in TEST_FILE_PATHS:
            print('Running file: {}'.format(test_file_path))
            with open(test_file_path) as test_file:
                input = read_input(test_file)
            output = test_function(input)
            folder_path = os.path.join(TEST_RESULT_PATH, folder_name)
            output_file_path = os.path.join(
                folder_path,
                '{}_{}'.format(folder_name, os.path.basename(test_file_path))
            )
            with open(output_file_path, 'w') as output_file:
                write_output(output, output_file)
            # file_score = count_score(input, output)
            # print('Score for file: {}'.format(file_score))
            # total_score += file_score
        print('Total score: {}'.format(total_score))


if __name__ == '__main__':
    run_tests()
