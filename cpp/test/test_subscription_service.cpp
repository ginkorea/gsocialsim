#include "../include/subscription_service.h"
#include <cassert>
#include <iostream>

void test_subscribe_unsubscribe() {
    SubscriptionService svc;

    // Test subscribe
    svc.subscribe("agent1", SubscriptionType::CREATOR, "creator1", 1.0, 0);
    assert(svc.is_subscribed("agent1", SubscriptionType::CREATOR, "creator1"));
    assert(svc.get_subscription_strength("agent1", SubscriptionType::CREATOR, "creator1") == 1.0);

    // Test subscriber lookup
    auto subs = svc.get_subscribers(SubscriptionType::CREATOR, "creator1");
    assert(subs.size() == 1);
    assert(subs.count("agent1") == 1);

    // Test unsubscribe
    svc.unsubscribe("agent1", SubscriptionType::CREATOR, "creator1");
    assert(!svc.is_subscribed("agent1", SubscriptionType::CREATOR, "creator1"));

    std::cout << "✓ Subscribe/Unsubscribe test passed\n";
}

void test_multiple_subscriptions() {
    SubscriptionService svc;

    // Subscribe to multiple types
    svc.subscribe("agent1", SubscriptionType::CREATOR, "creator1", 1.0, 0);
    svc.subscribe("agent1", SubscriptionType::TOPIC, "politics", 0.8, 0);
    svc.subscribe("agent1", SubscriptionType::OUTLET, "news_org", 0.6, 0);

    auto subs = svc.get_subscriptions("agent1");
    assert(subs.size() == 3);

    // Test subscriber counts
    assert(svc.subscriber_count(SubscriptionType::CREATOR, "creator1") == 1);
    assert(svc.subscriber_count(SubscriptionType::TOPIC, "politics") == 1);

    std::cout << "✓ Multiple subscriptions test passed\n";
}

void test_subscription_strength() {
    SubscriptionService svc;

    // Subscribe with strength
    svc.subscribe("agent1", SubscriptionType::CREATOR, "creator1", 0.5, 0);
    assert(svc.get_subscription_strength("agent1", SubscriptionType::CREATOR, "creator1") == 0.5);

    // Update strength (re-subscribe)
    svc.subscribe("agent1", SubscriptionType::CREATOR, "creator1", 0.9, 0);
    assert(svc.get_subscription_strength("agent1", SubscriptionType::CREATOR, "creator1") == 0.9);

    std::cout << "✓ Subscription strength test passed\n";
}

void test_bidirectional_lookup() {
    SubscriptionService svc;

    // Create subscription network
    svc.subscribe("agent1", SubscriptionType::CREATOR, "creator1", 1.0, 0);
    svc.subscribe("agent2", SubscriptionType::CREATOR, "creator1", 1.0, 0);
    svc.subscribe("agent3", SubscriptionType::CREATOR, "creator1", 1.0, 0);

    // Test forward lookup (agent -> subscriptions)
    auto agent1_subs = svc.get_subscriptions("agent1");
    assert(agent1_subs.size() == 1);

    // Test reverse lookup (creator -> subscribers)
    auto creator1_subs = svc.get_subscribers(SubscriptionType::CREATOR, "creator1");
    assert(creator1_subs.size() == 3);
    assert(creator1_subs.count("agent1") == 1);
    assert(creator1_subs.count("agent2") == 1);
    assert(creator1_subs.count("agent3") == 1);

    std::cout << "✓ Bidirectional lookup test passed\n";
}

int main() {
    std::cout << "Testing SubscriptionService...\n";

    test_subscribe_unsubscribe();
    test_multiple_subscriptions();
    test_subscription_strength();
    test_bidirectional_lookup();

    std::cout << "\n✅ All SubscriptionService tests passed!\n";
    return 0;
}
