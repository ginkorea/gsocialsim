#include "feed_queue.h"

#include <cmath>

static inline double clamp01(double v) {
    if (v < 0.0) return 0.0;
    if (v > 1.0) return 1.0;
    return v;
}

static double recency_score(int tick, int current_tick) {
    int age = current_tick - tick;
    if (age <= 0) return 1.0;
    return 1.0 / (1.0 + static_cast<double>(age));
}

void FeedPriorityQueue::push(
    const Content* content,
    int tick,
    int current_tick,
    double engagement,
    double proximity,
    double mutual_score) {
    if (!content) return;
    FeedItem item;
    item.content = content;
    item.tick = tick;
    item.engagement = clamp01(engagement);
    item.proximity = clamp01(proximity);
    item.mutual_score = clamp01(mutual_score);
    double recency = recency_score(tick, current_tick);
    item.score = (recency_weight_ * recency) +
                 (engagement_weight_ * item.engagement) +
                 (proximity_weight_ * item.proximity) +
                 (mutual_weight_ * item.mutual_score);
    heap_.push(item);
}

bool FeedPriorityQueue::empty() const {
    return heap_.empty();
}

size_t FeedPriorityQueue::size() const {
    return heap_.size();
}

FeedItem FeedPriorityQueue::pop() {
    FeedItem top = heap_.top();
    heap_.pop();
    return top;
}

std::vector<FeedItem> FeedPriorityQueue::drain() {
    std::vector<FeedItem> out;
    out.reserve(heap_.size());
    while (!heap_.empty()) {
        out.push_back(pop());
    }
    return out;
}

void FeedPriorityQueue::clear() {
    while (!heap_.empty()) {
        heap_.pop();
    }
}
