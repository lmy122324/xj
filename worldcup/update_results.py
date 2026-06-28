# -*- coding: utf-8 -*-
"""Update match results for past matches and update accuracy tracking"""
import json
from datetime import datetime

DATA_PATH = r'C:\Users\19916\Desktop\xj-local\worldcup\data.json'

with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

# Actual results from Yahoo Sports article (June 27 group stage / June 28 CST)
actual_results = {
    '克罗地亚|加纳': {'result': '克罗地亚胜', 'score': '克罗地亚 2-1 加纳', 'home_score': 2, 'away_score': 1},
    '巴拿马|英格兰': {'result': '英格兰胜', 'score': '英格兰 2-0 巴拿马', 'home_score': 0, 'away_score': 2},
    '哥伦比亚|葡萄牙': {'result': '平', 'score': '哥伦比亚 0-0 葡萄牙', 'home_score': 0, 'away_score': 0},
    '刚果(金)|乌兹别克斯坦': {'result': '刚果(金)胜', 'score': '刚果(金) 3-1 乌兹别克斯坦', 'home_score': 3, 'away_score': 1},
    '阿尔及利亚|奥地利': {'result': '平', 'score': '阿尔及利亚 3-3 奥地利', 'home_score': 3, 'away_score': 3},
    '约旦|阿根廷': {'result': '阿根廷胜', 'score': '阿根廷 3-1 约旦', 'home_score': 1, 'away_score': 3},
}

accuracy = data.get('prediction_accuracy', {
    'total_matches': 0, 'correct_h2h': 0, 'accuracy_rate': '追踪中',
    'history': [{'date': '06/23', 'note': '首轮预测开始'}]
})

for match in data['matches']:
    key = match['home'] + '|' + match['away']
    if key in actual_results:
        res = actual_results[key]
        old_result = match.get('result')
        match['result'] = res['result']
        match['actual_score'] = res['score']
        
        # Check if we had a prediction for this match
        analyses = match.get('analyses', [])
        if analyses:
            # Get latest prediction
            latest = analyses[-1]
            predicted_result = latest.get('text', '')
            # Extract predicted direction
            if '预测方向：' in predicted_result:
                pred_direction = predicted_result.split('预测方向：')[1].split(' |')[0].strip()
                
                actual = res['result']
                is_correct = 1 if pred_direction == actual else 0
                
                accuracy['total_matches'] = accuracy.get('total_matches', 0) + 1
                accuracy['correct_h2h'] = accuracy.get('correct_h2h', 0) + is_correct
                
                rate = accuracy['correct_h2h'] / accuracy['total_matches'] * 100 if accuracy['total_matches'] > 0 else 0
                accuracy['accuracy_rate'] = f'{rate:.1f}%'
                
                accuracy.setdefault('history', []).append({
                    'date': match['date'],
                    'match': f'{match["home"]} vs {match["away"]}',
                    'predicted': pred_direction,
                    'actual': actual,
                    'correct': is_correct == 1,
                    'cumulative_rate': f'{rate:.1f}%'
                })
                
                print(f'  {match["home"]} vs {match["away"]}: 预测={pred_direction}, 实际={actual}, {"✅" if is_correct else "❌"}')
        
        print(f'✅ {match["home"]} vs {match["away"]}: {match["result"]}')

print()
print(f'预测准确率: {accuracy["correct_h2h"]}/{accuracy["total_matches"]} = {accuracy["accuracy_rate"]}')

data['prediction_accuracy'] = accuracy

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print()
print('✅ 结果已更新保存')
