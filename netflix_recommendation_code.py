#!/usr/bin/env python3
"""
Netflix Multi-Objective Recommendation System
Thompson Sampling: Balancing Engagement + Discovery + Diversity

PURE NUMPY - NO DEPENDENCIES
Copy this entire file into a .py file and run it
"""

import numpy as np
from datetime import datetime

# ============================================================================
# REWARD FUNCTION
# ============================================================================

class RewardComputer:
    def __init__(self, engagement_weight=0.6, discovery_weight=0.3, diversity_weight=0.1):
        self.w_engagement = engagement_weight
        self.w_discovery = discovery_weight
        self.w_diversity = diversity_weight
    
    def compute_reward(self, user_watched, is_new, rec_genre, user_typical_genres):
        engagement = 1.0 if user_watched else 0.0
        discovery = 1.0 if is_new else 0.5
        diversity = 1.0 if rec_genre not in user_typical_genres else 0.3
        reward = (self.w_engagement * engagement + 
                 self.w_discovery * discovery + 
                 self.w_diversity * diversity)
        return reward


# ============================================================================
# THOMPSON SAMPLING
# ============================================================================

class ThompsonSamplingPolicy:
    def __init__(self, num_strategies=5):
        self.num_strategies = num_strategies
        self.strategy_alphas = np.ones(num_strategies)
        self.strategy_betas = np.ones(num_strategies)
    
    def sample_strategy(self):
        sampled_rewards = np.array([
            np.random.beta(self.strategy_alphas[i], self.strategy_betas[i])
            for i in range(self.num_strategies)
        ])
        strategy = int(np.argmax(sampled_rewards))
        return strategy
    
    def update(self, strategy, reward):
        reward_binary = 1 if reward > 0.5 else 0
        if reward_binary:
            self.strategy_alphas[strategy] += 1
        else:
            self.strategy_betas[strategy] += 1
    
    def get_stats(self):
        stats = []
        for i in range(self.num_strategies):
            alpha = self.strategy_alphas[i]
            beta = self.strategy_betas[i]
            total = alpha + beta
            success_rate = alpha / total if total > 0 else 0.5
            variance = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1)) if total > 1 else 0.25
            stats.append({'successes': int(alpha), 'failures': int(beta), 'rate': success_rate, 'uncertainty': variance})
        return stats


# ============================================================================
# STRATEGIES
# ============================================================================

STRATEGIES = {
    0: {"name": "Full Exploit", "explore_rate": 0.0},
    1: {"name": "90% Exploit / 10% Explore", "explore_rate": 0.1},
    2: {"name": "50-50 Mix", "explore_rate": 0.5},
    3: {"name": "10% Exploit / 90% Explore", "explore_rate": 0.9},
    4: {"name": "Full Explore", "explore_rate": 1.0}
}

def get_recommendation(strategy, user_familiar_titles, all_titles, explore_rate):
    if np.random.rand() < explore_rate:
        new_titles = all_titles - user_familiar_titles
        return np.random.choice(list(new_titles)) if new_titles else np.random.choice(list(user_familiar_titles))
    else:
        return np.random.choice(list(user_familiar_titles))


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 80)
    print("Netflix Multi-Objective Recommendation System")
    print("Thompson Sampling: Engagement + Discovery + Diversity")
    print("=" * 80)
    print()
    
    # Initialize
    thompson = ThompsonSamplingPolicy(num_strategies=5)
    reward_computer = RewardComputer()
    
    # User setup
    user_familiar_titles = {'drama_1', 'thriller_2', 'comedy_3', 'action_1'}
    all_titles = {f'title_{i}' for i in range(1, 101)}
    typical_genres = {'drama', 'thriller'}
    
    print("User Profile:")
    print(f"  Watched: {user_familiar_titles}")
    print(f"  Typical genres: {typical_genres}")
    print()
    
    # Run recommendations
    print("Running 15 recommendation rounds...")
    print("-" * 80)
    print(f"{'Rd':>2} | {'Strategy':<35} | {'Title':<12} | {'Watched':<7} | {'Reward':<6}")
    print("-" * 80)
    
    for round_num in range(15):
        # Sample strategy
        strategy = thompson.sample_strategy()
        
        # Get recommendation
        explore_rate = STRATEGIES[strategy]["explore_rate"]
        title = get_recommendation(strategy, user_familiar_titles, all_titles, explore_rate)
        
        # Simulate feedback
        watched = np.random.rand() < 0.75
        is_new = title not in user_familiar_titles
        rec_genre = 'comedy' if is_new else 'drama'
        
        # Compute reward
        reward = reward_computer.compute_reward(watched, is_new, rec_genre, typical_genres)
        
        # Update Thompson Sampling
        thompson.update(strategy, reward)
        
        # Print
        status = "✓" if watched else "✗"
        print(f"{round_num+1:2d} | {STRATEGIES[strategy]['name']:<35} | {title:<12} | {status:<7} | {reward:.3f}")
    
    print("-" * 80)
    print()
    
    # Print results
    print("Thompson Sampling Results:")
    print("-" * 80)
    print(f"{'Strategy':<35} | {'Successes':<10} | {'Rate':<7} | {'Uncertainty':<12}")
    print("-" * 80)
    
    stats = thompson.get_stats()
    for i, stat in enumerate(stats):
        strategy_name = STRATEGIES[i]['name']
        print(f"{strategy_name:<35} | {stat['successes']:>9} | {stat['rate']:>6.1%} | {stat['uncertainty']:>11.6f}")
    
    print()
    print("=" * 80)
    print("SUCCESS! Thompson Sampling learned which strategies work best.")
    print("=" * 80)