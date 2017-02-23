import collections


def greedy(input, request_priority, cache_chooser):
    output = collections.defaultdict(list)
    space_left = collections.defaultdict(lambda: input.cache_size)

    for request in sorted(input.requests, key=request_priority, reverse=True):
        endpoint = input.endpoints[request.endpoint_id]
        video_size = input.video_sizes[request.video_id]
        available_cache_space_left = {
            cache_id: space_left[cache_id]
            for cache_id, latency
            in endpoint.cache_latencies.items()
            if space_left[cache_id] >= video_size
        }
        chosed_cache_id = cache_chooser(video_size, available_cache_space_left)
        output[chosed_cache_id].append(request.video_id)

    return output


# request priorities

def priority_count(request):
    return request.count


# cache choosers

def best_fit(video_size, available_cache_space_left):
    return min(
        available_cache_space_left.items(),
        key=lambda pair: pair[1]
    )[0]
