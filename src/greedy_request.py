import collections


def greedy(request_priority, cache_chooser, input):
    output = collections.defaultdict(set)
    space_left = collections.defaultdict(lambda: input.cache_size)

    def sort_key(request):
        return request_priority(
            request=request,
            video_size=input.video_sizes[request.video_id],
        )

    for request in sorted(input.requests, key=sort_key, reverse=True):
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
            endpoint=endpoint,
        )
        output[chosen_cache_id].add(request.video_id)
        space_left[chosen_cache_id] -= video_size
    return output


# request priorities

def priority_count(request, **_):
    return request.count


def priority_video_small(video_size, **_):
    return -video_size


def priority_video_big(video_size, **_):
    return video_size


# cache choosers

def best_fit(available_cache_space_left, **_):
    return min(
        available_cache_space_left.items(),
        key=lambda pair: pair[1]
    )[0]


def min_latency(available_cache_space_left, endpoint, **_):
    return min(
        available_cache_space_left,
        key=lambda cache_id: endpoint.cache_latencies[cache_id]
    )

