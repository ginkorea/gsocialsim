#pragma once

#include <queue>
#include <vector>

#include "types.h"

struct FeedItem {
    const Content* content = nullptr;
    int tick = 0;
    double engagement = 0.0;  // per-agent or global proxy (e.g., social_proof)
    double proximity = 0.0;
    double score = 0.0;
};

class FeedPriorityQueue {
public:
    FeedPriorityQueue(double recency_weight = 0.4, double engagement_weight = 0.5, double proximity_weight = 0.1)
        : recency_weight_(recency_weight),
          engagement_weight_(engagement_weight),
          proximity_weight_(proximity_weight) {}

    void push(const Content* content, int tick, int current_tick, double engagement, double proximity);
    bool empty() const;
    size_t size() const;
    FeedItem pop();
    std::vector<FeedItem> drain();
    void clear();

private:
    struct Compare {
        bool operator()(const FeedItem& a, const FeedItem& b) const {
            return a.score < b.score;  // max-heap by score
        }
    };

    double recency_weight_ = 0.4;
    double engagement_weight_ = 0.5;
    double proximity_weight_ = 0.1;
    std::priority_queue<FeedItem, std::vector<FeedItem>, Compare> heap_;
};
