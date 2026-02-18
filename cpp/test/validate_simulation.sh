#!/bin/bash
# Validation script for gsocialsim
# Tests various simulation configurations and validates outputs

set -e  # Exit on error

echo "================================"
echo "GSOCIALSIM Validation Suite"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

EXECUTABLE="../build/gsocialsim_cpp"
ERRORS=0

# Helper function to run test
run_test() {
    local test_name=$1
    shift
    local args="$@"

    echo -n "Testing: $test_name... "

    if $EXECUTABLE $args > /tmp/test_output.txt 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        cat /tmp/test_output.txt
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Test 1: Basic simulation (minimal agents)
echo "=== Phase 1: Basic Functionality ==="
run_test "Minimal simulation (5 agents, 5 ticks)" \
    --agents 5 --avg-following 2 --ticks 5

run_test "Small simulation (10 agents, 10 ticks)" \
    --agents 10 --avg-following 3 --ticks 10

run_test "Medium simulation (50 agents, 20 ticks)" \
    --agents 50 --avg-following 5 --ticks 20

echo ""

# Test 2: Network configurations
echo "=== Phase 2: Network Configurations ==="
run_test "Random network mode" \
    --agents 20 --avg-following 4 --ticks 10 --network-mode random

run_test "Grouped network mode" \
    --agents 20 --avg-following 4 --ticks 10 --network-mode groups

echo ""

# Test 3: Subscription service validation
echo "=== Phase 3: Subscription Service ==="
echo "Checking subscription creation..."
$EXECUTABLE --agents 20 --avg-following 5 --ticks 5 > /tmp/sub_test.txt 2>&1

if grep -q "creator subscriptions" /tmp/sub_test.txt; then
    echo -e "${GREEN}✓ Subscriptions initialized${NC}"
else
    echo -e "${RED}✗ Subscription initialization failed${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 4: Network manager validation
echo ""
echo "=== Phase 4: Network Manager ==="
echo "Checking network layers..."
if grep -q "Registered 2 network layers" /tmp/sub_test.txt; then
    echo -e "${GREEN}✓ Network layers registered${NC}"
else
    echo -e "${RED}✗ Network layer registration failed${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 5: Population layer validation
echo ""
echo "=== Phase 5: Population Layer ==="
echo "Checking population initialization..."
if grep -q "Population layer.*segments" /tmp/sub_test.txt; then
    echo -e "${GREEN}✓ Population layer initialized${NC}"

    # Extract segment count
    SEGMENTS=$(grep "Population layer" /tmp/sub_test.txt | grep -oP '\d+(?= segments)')
    if [ "$SEGMENTS" = "5" ]; then
        echo -e "${GREEN}✓ Correct number of segments (5)${NC}"
    else
        echo -e "${YELLOW}⚠ Unexpected segment count: $SEGMENTS (expected 5)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Population layer not initialized (geo may be disabled)${NC}"
fi

# Test 6: Performance test
echo ""
echo "=== Phase 6: Performance Baseline ==="
echo "Running performance test (100 agents, 50 ticks)..."

START_TIME=$(date +%s.%N)
$EXECUTABLE --agents 100 --avg-following 10 --ticks 50 > /tmp/perf_test.txt 2>&1
END_TIME=$(date +%s.%N)

DURATION=$(echo "$END_TIME - $START_TIME" | bc)
echo "Total time: ${DURATION}s"

# Extract simulation time
SIM_TIME=$(grep "simulation time:" /tmp/perf_test.txt | grep -oP '\d+\.\d+' | head -1)
TICKS_PER_SEC=$(echo "scale=2; 50 / $SIM_TIME" | bc)

echo "Simulation time: ${SIM_TIME}s"
echo "Throughput: ${TICKS_PER_SEC} ticks/second"

if (( $(echo "$TICKS_PER_SEC > 10" | bc -l) )); then
    echo -e "${GREEN}✓ Performance acceptable (>10 ticks/s)${NC}"
else
    echo -e "${YELLOW}⚠ Performance below target (<10 ticks/s)${NC}"
fi

# Test 7: Determinism check
echo ""
echo "=== Phase 7: Determinism Validation ==="
echo "Running same simulation twice with same seed..."

$EXECUTABLE --agents 20 --avg-following 4 --ticks 10 --seed 42 > /tmp/det1.txt 2>&1
$EXECUTABLE --agents 20 --avg-following 4 --ticks 10 --seed 42 > /tmp/det2.txt 2>&1

if diff /tmp/det1.txt /tmp/det2.txt > /dev/null; then
    echo -e "${GREEN}✓ Deterministic execution (same seed → same output)${NC}"
else
    echo -e "${RED}✗ Non-deterministic execution detected${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 8: Scale test
echo ""
echo "=== Phase 8: Scale Test ==="
run_test "Large simulation (500 agents, 10 ticks)" \
    --agents 500 --avg-following 20 --ticks 10

# Summary
echo ""
echo "================================"
echo "VALIDATION SUMMARY"
echo "================================"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ $ERRORS test(s) failed${NC}"
    exit 1
fi
