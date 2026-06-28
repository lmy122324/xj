# -*- coding: utf-8 -*-
"""Fix comparison logic for predictions vs actual results"""
import json

DATA_PATH = r'C:\Users\19916\Desktop\xj-local\worldcup\data.json'

with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

actual_results = {
    '克罗地亚|加纳': {'result': '克罗地亚胜', 'predicted_direction': '克罗地亚'},
    '巴拿马|英格兰': {'result': '英格兰胜', 'predicted_direction': 'Draw'},
    '哥伦比亚|葡萄牙': {'result': '平', 'predicted_direction': 'Draw'},
    '刚果(金)|乌兹别克斯坦': {'result': '刚果(金)胜', 'predicted_direction': '刚果(金)'},
    '阿尔及利亚|奥地利': {'result': '平', 'predicted_direction': '奥地利'},
    '约旦|阿根廷': {'result': '阿根廷胜', 'predicted_direction': 'Draw'},
}

accuracy = data.get('prediction_accuracy', {
    'total_matches': 0, 'correct_h2h': 0, 'accuracy_rate': '追踪中',
    'history': [{'date': '06/23', 'note': '首轮预测开始'}]
})

def normalize(pred, actual):
    """Normalize both to comparable format"""
    # Extract base from actual result (e.g. '克罗地亚胜' -> '克罗地亚', '平' -> 'Draw')
    if actual == '平':
        actual_base = 'Draw'
    elif actual.endswith('胜'):
        actual_base = actual[:-1]  # Remove '胜'
    else:
        actual_base = actual
    
    # For comparison: if pred is "Croatia" (English) and actual_base is "克罗地亚" (Chinese), need mapping
    return pred, actual_base

def is_correct(pred, actual):
    """Check if prediction matched actual result"""
    if actual == '平':
        return pred == 'Draw'
    if actual.endswith('胜'):
        team = actual[:-1]
        return pred == team
    return False

results_log = []
correct_count = 0
total_count = 0

for match in data['matches']:
    key = match['home'] + '|' + match['away']
    if key in actual_results:
        res = actual_results[key]
        analyses = match.get('analyses', [])
        if analyses:
            latest = analyses[-1]
            predicted_text = latest.get('text', '')
            
            # Extract predicted direction
            pred_direction = None
            if '预测方向：' in predicted_text:
                pred_direction = predicted_text.split('预测方向：')[1].split(' |')[0].strip()
            
            if pred_direction:
                actual = res['result']
                correct = is_correct(pred_direction, actual)
                total_count += 1
                if correct:
                    correct_count += 1
                
                results_log.append({
                    'match': f'{match["home"]} vs {match["away"]}',
                    'predicted': pred_direction,
                    'actual': actual,
                    'correct': correct
                })
                
                emoji = '✅' if correct else '❌'
                print(f'  {match["home"]} vs {match["away"]}: 预测={pred_direction}, 实际={actual} {emoji}')

# Recalculate accuracy
accuracy['total_matches'] = total_count
accuracy['correct_h2h'] = correct_count
rate = correct_count / total_count * 100 if total_count > 0 else 0
accuracy['accuracy_rate'] = f'{rate:.1f}%'

# Update history
for r in results_log:
    accuracy.setdefault('history', []).append({
        'date': match['date'],
        'match': r['match'],
        'predicted': r['predicted'],
        'actual': r['actual'],
        'correct': r['correct'],
        'cumulative_rate': f'{round(correct_count/total_count*100, 1)}%' if total_count > 0 else '0%'
    })

data['prediction_accuracy'] = accuracy

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\n📊 预测准确率: {correct_count}/{total_count} = {accuracy["accuracy_rate"]}')
print('✅ 已保存')
