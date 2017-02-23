import collections


def greedy_video_cache(input):
    output = collections.defaultdict(set)
    space_left = collections.defaultdict(lambda: input.cache_size)

    def calculate_edge_profits():
        result = collections.defaultdict(int)

        for request in input.requests:
            video_id = request.video_id
            video_size = input.video_sizes[video_id]
            endpoint = input.endpoints[request.endpoint_id]

            current_latency = endpoint.data_center_latency
            for cache_id, cache_latency in endpoint.cache_latencies.items():
                if video_id in output[cache_id] and \
                        current_latency > cache_latency:
                    current_latency = cache_latency

            for cache_id, cache_latency in endpoint.cache_latencies.items():
                if space_left[cache_id] >= video_size:
                    result[(video_id, cache_id)] += \
                        (current_latency - cache_latency) * request.count

        return result

    while True:
        edge_profits = calculate_edge_profits()
        if not edge_profits:
            return output
        edge, _ = max(edge_profits.items(), key=lambda pair: pair[1])
        video_id, cache_id = edge
        output[cache_id].add(video_id)
        space_left[cache_id] -= input.video_sizes[video_id]
