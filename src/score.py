

def _get_caches_with_video_id(cache_descriptions, video_id):
    cache_ids = []
    for cache_id, video_ids in cache_descriptions.items():
        if video_id in video_ids:
            cache_ids.append(cache_id)
    return cache_ids


def _count_score(requests, endpoints, cache_descriptions):
    score = 0
    total_requests = 0
    for request in requests:
        endpoint = endpoints[request.endpoint_id]
        cache_ids = _get_caches_with_video_id(cache_descriptions, request.video_id)
        min_latency = min([endpoint.cache_latencies[cache_id] for cache_id in cache_ids])
        latency_diff = endpoint.data_center_latency - min_latency
        score += request.count * latency_diff
    return (score * 1000) // total_requests


def run_count_score(input, output):
    return _count_score(input.requests, input.endpoints, output)
