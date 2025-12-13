"""
Script để test Parameter Sensitivity - Phân tích ảnh hưởng của min_support
Nhóm 11 - Data Mining Week 01
"""

import pandas as pd
import time
import sys
sys.path.insert(0, 'src')

from apriori_library import AssociationRulesMiner

def test_parameter_sensitivity():
    """
    Test thuật toán Apriori với các giá trị min_support khác nhau
    """
    
    print("="*70)
    print("PARAMETER SENSITIVITY ANALYSIS - MIN_SUPPORT")
    print("="*70)
    
    # Load basket data
    print("\nLoading basket data...")
    basket_bool = pd.read_parquet("data/processed/basket_bool.parquet")
    print(f"Loaded basket: {basket_bool.shape}")
    
    # Danh sách min_support cần test (bỏ 0.005 vì quá tốn memory)
    support_values = [0.01, 0.015, 0.02, 0.03]
    
    results = []
    
    for min_sup in support_values:
        print(f"\n{'='*70}")
        print(f"Testing min_support = {min_sup} ({min_sup*100}%)")
        print('='*70)
        
        start_time = time.time()
        
        try:
            # Initialize miner
            miner = AssociationRulesMiner(basket_bool=basket_bool)
            
            # Mine frequent itemsets
            print("Mining frequent itemsets...")
            freq_items = miner.mine_frequent_itemsets(
                min_support=min_sup,
                max_len=3
            )
            
            # Generate rules (không cần truyền freq_items vì đã lưu trong miner)
            print("Generating association rules...")
            rules = miner.generate_rules(
                metric="lift",
                min_threshold=1.0
            )
            
            # Filter rules (không cần truyền rules vì đã lưu trong miner)
            print("Filtering high-quality rules...")
            filtered = miner.filter_rules(
                min_support=min_sup,
                min_confidence=0.3,
                min_lift=1.2,
                max_len_antecedents=2,
                max_len_consequents=1
            )
            
            elapsed = time.time() - start_time
            
            # Collect stats
            result = {
                'min_support': min_sup,
                'frequent_itemsets': len(freq_items),
                'rules_before_filter': len(rules),
                'rules_after_filter': len(filtered),
                'avg_confidence': filtered['confidence'].mean() if len(filtered) > 0 else 0,
                'avg_lift': filtered['lift'].mean() if len(filtered) > 0 else 0,
                'max_lift': filtered['lift'].max() if len(filtered) > 0 else 0,
                'time_seconds': elapsed
            }
            results.append(result)
            
            # Print results
            print(f"\n✅ RESULTS:")
            print(f"   Frequent itemsets: {len(freq_items):,}")
            print(f"   Rules (before filter): {len(rules):,}")
            print(f"   Rules (after filter): {len(filtered):,}")
            print(f"   Avg Confidence: {result['avg_confidence']:.3f}")
            print(f"   Avg Lift: {result['avg_lift']:.3f}")
            print(f"   Max Lift: {result['max_lift']:.3f}")
            print(f"   Time: {elapsed:.2f}s")
            
            if len(filtered) > 0:
                print(f"\n📊 Top 5 rules by lift:")
                top_rules = filtered.sort_values('lift', ascending=False).head(5)
                for idx, row in top_rules.iterrows():
                    ant = ', '.join(list(row['antecedents']))
                    cons = ', '.join(list(row['consequents']))
                    print(f"   {ant} → {cons}")
                    print(f"      Support: {row['support']:.4f}, Conf: {row['confidence']:.3f}, Lift: {row['lift']:.3f}")
            else:
                print("\n⚠️ No rules found with current filters!")
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            result = {
                'min_support': min_sup,
                'frequent_itemsets': 0,
                'rules_before_filter': 0,
                'rules_after_filter': 0,
                'avg_confidence': 0,
                'avg_lift': 0,
                'max_lift': 0,
                'time_seconds': time.time() - start_time
            }
            results.append(result)
    
    # Summary table
    print("\n" + "="*70)
    print("SUMMARY COMPARISON")
    print("="*70)
    
    summary_df = pd.DataFrame(results)
    
    # Format for display
    summary_df['min_support'] = summary_df['min_support'].apply(lambda x: f"{x:.3f} ({x*100:.1f}%)")
    summary_df['avg_confidence'] = summary_df['avg_confidence'].apply(lambda x: f"{x:.3f}")
    summary_df['avg_lift'] = summary_df['avg_lift'].apply(lambda x: f"{x:.3f}")
    summary_df['max_lift'] = summary_df['max_lift'].apply(lambda x: f"{x:.3f}")
    summary_df['time_seconds'] = summary_df['time_seconds'].apply(lambda x: f"{x:.2f}s")
    
    print(summary_df.to_string(index=False))
    
    # Save to CSV (raw data)
    summary_raw = pd.DataFrame(results)
    summary_raw.to_csv("data/processed/parameter_sensitivity_results.csv", index=False)
    print("\n✅ Results saved to: data/processed/parameter_sensitivity_results.csv")
    
    # Visual comparison
    print("\n" + "="*70)
    print("VISUAL COMPARISON - Number of Rules After Filter")
    print("="*70)
    
    max_rules = max([r['rules_after_filter'] for r in results])
    if max_rules > 0:
        for result in results:
            bar_length = int((result['rules_after_filter'] / max_rules) * 40)
            bar = '█' * bar_length
            print(f"{result['min_support']:.3f}: {bar} ({result['rules_after_filter']})")
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    
    # Find optimal min_support
    valid_results = [r for r in results if r['rules_after_filter'] > 0]
    if valid_results:
        # Best balance: có nhiều luật nhưng không quá nhiều
        optimal = None
        for r in valid_results:
            if 50 <= r['rules_after_filter'] <= 200:
                optimal = r
                break
        
        if not optimal:
            # Fallback: chọn cái có nhiều luật nhất
            optimal = max(valid_results, key=lambda x: x['rules_after_filter'])
        
        print(f"\n⭐ RECOMMENDED min_support: {optimal['min_support']:.3f} ({optimal['min_support']*100:.1f}%)")
        print(f"   Reasons:")
        print(f"   ✓ Generates {optimal['rules_after_filter']} quality rules")
        print(f"   ✓ Average Lift: {optimal['avg_lift']:.3f}")
        print(f"   ✓ Processing time: {optimal['time_seconds']:.2f}s")
        print(f"   ✓ Balanced between quantity and quality")
    
    print("\n" + "="*70)
    print("Analysis complete! Check Parameter_Sensitivity_Analysis.md for details.")
    print("="*70)

if __name__ == "__main__":
    test_parameter_sensitivity()
