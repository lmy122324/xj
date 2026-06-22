import json

# Actual results from nowscore.com
results = {
    "荷兰 vs 瑞典": {"home": "荷兰", "away": "瑞典", "score": "5-1", "winner": "荷兰胜", "date": "06/21"},
    "德国 vs 科特迪瓦": {"home": "德国", "away": "科特迪瓦", "score": "2-1", "winner": "德国胜", "date": "06/21"},
    "厄瓜多尔 vs Curaçao": {"home": "厄瓜多尔", "away": "Curaçao", "score": "0-0", "winner": "平", "date": "06/21"},
    "突尼斯 vs 日本": {"home": "突尼斯", "away": "日本", "score": "0-4", "winner": "日本胜", "date": "06/21"},
}

with open('C:/Users/19916/Desktop/xj-local/worldcup/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data['matches']

# Step 1: Find matches that need results
for match in matches:
    key = f"{match['home']} vs {match['away']}"
    if key in results and match.get('result') is None:
        res = results[key]
        match['result'] = res['winner']
        match['score'] = res['score']
        print(f"✅ Updated: {key} -> {res['winner']} ({res['score']})")

# Step 2: Check prediction accuracy
correct_h2h = 0
total = 0
verified_count = 0

for match in matches:
    key = f"{match['home']} vs {match['away']}"
    r = match.get('result')
    if r is None or match.get('verified'):
        continue
    
    # Get latest analysis
    analyses = match.get('analyses', [])
    if not analyses:
        continue
    
    # Take the latest analysis's deepAnalysis predictedResult
    latest = analyses[-1]
    da = latest.get('deepAnalysis', {})
    predicted = da.get('predictedResult')
    
    if predicted:
        total += 1
        # Simple direction comparison
        actual = r  # e.g. "荷兰胜", "平", "日本胜"
        is_correct = (predicted == actual)
        # Also check if both indicate same direction even if wording differs
        # "荷兰胜" vs "荷兰胜" ✅, "平" vs "Draw (predicted)"
        if is_correct:
            correct_h2h += 1
            
        match['verified'] = True
        verified_count += 1
        print(f"  🎯 {key}: Predicted={predicted}, Actual={actual} {'✅' if is_correct else '❌'}")

# Step 3: Update prediction_accuracy
acc = data.get('prediction_accuracy', {})
if not acc:
    acc = {"total_matches": 0, "correct_h2h": 0, "accuracy_rate": "0.0%", "history": []}

old_total = acc.get('total_matches', 0)
old_correct = acc.get('correct_h2h', 0)

acc['total_matches'] = old_total + total
acc['correct_h2h'] = old_correct + correct_h2h
acc['accuracy_rate'] = f"{(acc['correct_h2h']/acc['total_matches']*100):.1f}%" if acc['total_matches'] > 0 else "0.0%"

# Add history entry
history = acc.get('history', [])
history.append({"date": "06/21", "rate": round(correct_h2h/total*100) if total > 0 else 0})
acc['history'] = history

data['prediction_accuracy'] = acc

print(f"\n--- Summary ---")
print(f"Verified this batch: {verified_count} matches")
print(f"Correct: {correct_h2h}/{total} = {acc['accuracy_rate']}")
print(f"History: {json.dumps(history)}")

# Save updated data
with open('C:/Users/19916/Desktop/xj-local/worldcup/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ data.json updated and saved!")
