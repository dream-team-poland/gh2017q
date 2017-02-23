from collections import Counter, defaultdict
from functools import partial


def _sort_caches_by_requests(endpoints, requests):
    cache_to_requests_count = Counter()
    cache_to_requests = defaultdict(list)
    for request in requests:
        endpoint = endpoints[request.endpoint_id]
        for cache_id in endpoint.cache_latencies.keys():
            cache_to_requests_count[cache_id] += request.count
            cache_to_requests[cache_id].append(request)
    most_common = cache_to_requests_count.most_common()
    return [cache_id for cache_id, count in most_common], cache_to_requests


def request_score(cache_id, endpoints, request):
    endpoint = endpoints[request.endpoint_id]
    return request.count * (endpoint.cache_latencies[cache_id] - endpoint.data_center_latency)


def _get_videos_for_cache(cache_id, requests_for_cache, cache_size, endpoints, video_sizes):
    videos = []
    size_remaining = cache_size
    score_fun = partial(request_score, cache_id, endpoints)
    requests_for_cache.sort(key=score_fun, reverse=True)
    for request in requests_for_cache:
        size = video_sizes[request.video_id]
        if size <= size_remaining:
            videos.append(request.video_id)
            size_remaining -= size
        else:
            continue
    return videos


def greedy_per_cache(input):
    cache_ids, cache_to_requests = _sort_caches_by_requests(input.endpoints, input.requests)
    output = {}
    for cache_id in cache_ids:
        output[cache_id] = _get_videos_for_cache(
            cache_id,
            cache_to_requests[cache_id],
            input.cache_size,
            input.endpoints,
            input.video_sizes
        )
    return output
