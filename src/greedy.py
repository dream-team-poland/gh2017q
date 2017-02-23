import collections


def greedy(input, request_priority, cache_chooser):
    output = collections.defaultdict(set)
    space_left = collections.defaultdict(lambda: input.cache_size)

    for request in sorted(input.requests, key=request_priority, reverse=True):
        endpoint = input.endpoints[request.endpoint_id]
        video_size = input.video_sizes[request.video_id]
        if any(
            request.video_id in output[cache_id]
            for cache_id in endpoint.cache_latencies
        ):
            continue
        available_cache_space_left = {
            cache_id: space_left[cache_id]
            for cache_id
            in endpoint.cache_latencies
            if space_left[cache_id] >= video_size
        }
        if not available_cache_space_left:
            continue
        chosen_cache_id = cache_chooser(
            available_cache_space_left=available_cache_space_left,
        )
        output[chosen_cache_id].add(request.video_id)
        space_left[chosen_cache_id] -= video_size


# request priorities

def priority_count(request):
    return request.count


# cache choosers

def best_fit(available_cache_space_left, **_):
    return min(
        available_cache_space_left.items(),
        key=lambda pair: pair[1]
    )[0]
