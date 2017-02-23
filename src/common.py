import collections
import sys


Input = collections.namedtuple(
    "Input",
    [
        "video_sizes",
        "endpoints",
        "requests",
        "cache_count",
        "cache_size",
    ],
)


Endpoint = collections.namedtuple(
    "Endpoint",
    [
        "data_center_latency",
        "cache_latencies",  # dict: cache_id -> latency
    ],
)


Request = collections.namedtuple(
    "Request",
    [
        "video_id",
        "endpoint_id",
        "count",
    ]
)


def read_input(file):
    return parse_input(map(int, line.strip().split()) for line in file)


def parse_input(rows):
    video_count, endpoint_count, request_count, cache_count, cache_size = \
        next(rows)

    *video_sizes, = next(rows)

    endpoints = [
        parse_endpoint(rows)
        for _ in range(endpoint_count)
    ]

    requests = [
        Request(*next(rows))
        for _ in range(request_count)
    ]

    return Input(
        video_sizes=video_sizes,
        endpoints=endpoints,
        requests=requests,
        cache_count=cache_count,
        cache_size=cache_size,
    )


def parse_endpoint(rows):
    data_center_latency, cache_count = next(rows)
    return Endpoint(
        data_center_latency=data_center_latency,
        cache_latencies=dict(next(rows) for _ in range(cache_count))
    )


# output: dict: cache_id -> list of video_ids

def validate_output(input, output):
    cache_size = input.cache_size
    video_sizes = input.video_sizes
    for cache_id, video_ids in output.items():
        overall_size = sum([video_sizes[id_] for id_ in video_ids])
        if overall_size > cache_size:
            raise ValueError('Videos size exceeded for cache {}: {}'.format(cache_id, overall_size))


def output_rows(output):
    yield [len(output)]
    for cache_id, video_ids in output.items():
        yield [cache_id] + video_ids


def write_output(output, file=sys.stdout):
    for row in output_rows(output):
        print(" ".join(map(str, row)), file=file)
