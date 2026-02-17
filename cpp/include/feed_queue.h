#pragma once

#include <queue>
#include <vector>

#include "types.h"

struct FeedItem {
    const Content* content = nullptr;
    int tick = 0;
    double engagement = 0.0;  // per-agent or global proxy (e.g., social_proof)
    double score = 0.0;
};

class FeedPriorityQueue {
public:
    FeedPriorityQueue(double recency_weight = 0.4, double engagement_weight = 0.6)
        : recency_weight_(recency_weight), engagement_weight_(engagement_weight) {}

    void push(const Content* content, int tick, int current_tick, double engagement);
    bool empty() const;
    size_t size() const;
    FeedItem pop();
    std::vector<FeedItem> drain();

private:
    struct Compare {
        bool operator()(const FeedItem& a, const FeedItem& b) const {
            return a.score < b.score;  // max-heap by score
        }
    };

    double recency_weight_ = 0.4;
    double engagement_weight_ = 0.6;
    std::priority_queue<FeedItem, std::vector<FeedItem>, Compare> heap_;
};
