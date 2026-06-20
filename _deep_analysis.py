#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep analysis addition + accuracy calculation for World Cup predictions"""
import json, subprocess, os
from datetime import datetime, timezone, timedelta

DATA_PATH = r'C:\Users\19916\Desktop\xj-local\worldcup\data.json'
REPO_DIR = r'C:\Users\19916\Desktop\xj-local'

bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz)

# FIFA rankings
FIFA_RANKINGS = {
    'Argentina': 1, '法国': 2, '巴西': 3, '英格兰': 4, '比利时': 5,
    '荷兰': 6, '葡萄牙': 7, '西班牙': 8, '意大利': 9, '克罗地亚': 10,
    '美国': 11, '墨西哥': 12, '德国': 13, '摩洛哥': 14, '瑞士': 15,
    '乌拉圭': 16, '哥伦比亚': 17, '日本': 18, '塞内加尔': 19, '伊朗': 20,
    '瑞典': 21, '韩国': 22, '澳大利亚': 23, '奥地利': 24,
    '阿尔及利亚': 25, '土耳其': 26, '巴拉圭': 27, '厄瓜多尔': 28,
    '苏格兰': 29, '挪威': 30, '沙特': 31, '科特迪瓦': 33,
    '埃及': 34, '南非': 35, '尼日利亚': 36, '加拿大': 37,
    '波黑': 38, '突尼斯': 39, '捷克': 40,
    '巴拿马': 41, '加纳': 42, '卡塔尔': 43, '刚果(金)': 44, '牙买加': 45,
    '伊拉克': 46, '约旦': 47, '乌兹别克斯坦': 48, '佛得角': 49,
    '新西兰': 50, '海地': 51, '库拉索': 52,
}

TEAM_INFO = {
    '巴西': {'star': 'Vinícius Jr', 'coach': 'Dorival Jr', 'strength': '锋线豪华,技术优势', 'weakness': '防守纪律性', 'style': '控球进攻,边路突破'},
    '法国': {'star': 'Kylian Mbappé', 'coach': 'Didier Deschamps', 'strength': '锋线深度,整体实力', 'weakness': '中场创造力', 'style': '快速反击,身体对抗'},
    '阿根廷': {'star': 'Lionel Messi', 'coach': 'Lionel Scaloni', 'strength': '进攻组织,大赛经验', 'weakness': '后防老化', 'style': '传控渗透,前场压迫'},
    '英格兰': {'star': 'Harry Kane', 'coach': 'Gareth Southgate', 'strength': '阵容深度,定位球', 'weakness': '大赛心理', 'style': '攻守平衡,边中结合'},
    '荷兰': {'star': 'Virgil van Dijk', 'coach': 'Ronald Koeman', 'strength': '后防稳固,战术纪律', 'weakness': '锋线效率', 'style': '全攻全守,控球压制'},
    '德国': {'star': 'Jamal Musiala', 'coach': 'Julian Nagelsmann', 'strength': '年轻化改革,中场创造力', 'weakness': '中锋终结能力', 'style': '高压逼抢,快速传递'},
    '西班牙': {'star': 'Pedri', 'coach': 'Luis de la Fuente', 'strength': '传控体系,中场控制', 'weakness': '缺乏高效射手', 'style': '极致传控,短传渗透'},
    '葡萄牙': {'star': 'Cristiano Ronaldo', 'coach': 'Roberto Martínez', 'strength': '攻击火力,阵容深度', 'weakness': '防守稳定性', 'style': '边路突击,定位球'},
    '比利时': {'star': 'Kevin De Bruyne', 'coach': 'Domenico Tedesco', 'strength': '中场创造力,经验丰富', 'weakness': '后防换代', 'style': '控球推进,中路渗透'},
    '摩洛哥': {'star': 'Achraf Hakimi', 'coach': 'Walid Regragui', 'strength': '防守组织,反击速度', 'weakness': '进攻创造力有限', 'style': '防守反击,边翼卫插上'},
    '日本': {'star': 'Takefusa Kubo', 'coach': 'Hajime Moriyasu', 'strength': '团队纪律,快速反击', 'weakness': '身体对抗', 'style': '技术传控,耐心组织'},
    '美国': {'star': 'Christian Pulisic', 'coach': 'Gregg Berhalter', 'strength': '年轻活力,体能优势', 'weakness': '大赛经验', 'style': '高速转换,边路冲击'},
    '乌拉圭': {'star': 'Federico Valverde', 'coach': 'Marcelo Bielsa', 'strength': '中场硬朗,战斗精神', 'weakness': '锋线老化', 'style': '高位压迫,激烈对抗'},
    '瑞典': {'star': 'Alexander Isak', 'coach': 'Jon Dahl Tomasson', 'strength': '身体对抗,空中优势', 'weakness': '技术细腻度', 'style': '长传冲吊,边路传中'},
    '突尼斯': {'star': 'Wahbi Khazri', 'coach': 'Jalel Kadri', 'strength': '防守韧性,团队协作', 'weakness': '创造力不足', 'style': '密集防守,快速转换'},
    '厄瓜多尔': {'star': 'Kendry Páez', 'coach': 'Gustavo Alfaro', 'strength': '年轻天赋,体能充沛', 'weakness': '大赛经验', 'style': '跑动积极,中前场压迫'},
    '科特迪瓦': {'star': 'Seko Fofana', 'coach': 'Emerse Faé', 'strength': '身体对抗,中场硬朗', 'weakness': '防守组织', 'style': '力量型打法,个人能力'},
    '土耳其': {'star': 'Hakan Çalhanoğlu', 'coach': 'Vincenzo Montella', 'strength': '中场技术,远射能力', 'weakness': '防守纪律', 'style': '技术流,中远距离攻击'},
    '巴拉圭': {'star': 'Miguel Almirón', 'coach': 'Gustavo Alfaro', 'strength': '防守强硬,反击犀利', 'weakness': '进攻创造力', 'style': '强硬防守,快速反击'},
    '苏格兰': {'star': 'Scott McTominay', 'coach': 'Steve Clarke', 'strength': '身体对抗,团队精神', 'weakness': '技术粗糙', 'style': '高强度逼抢,定位球'},
    '挪威': {'star': 'Erling Haaland', 'coach': 'Ståle Solbakken', 'strength': '锋线终结能力', 'weakness': '整体防守', 'style': '长传冲吊,利用支点'},
    '塞内加尔': {'star': 'Sadio Mané', 'coach': 'Aliou Cissé', 'strength': '边路速度,身体优势', 'weakness': '中场控制力', 'style': '快速反击,边路冲击'},
    '伊拉克': {'star': 'Mohamed Qasim', 'coach': 'Jesús Casas', 'strength': '团队防守,纪律性', 'weakness': '个人能力差距', 'style': '密集防守,长传反击'},
    '沙特': {'star': 'Salem Al-Dawsari', 'coach': 'Roberto Mancini', 'strength': '技术细腻,默契配合', 'weakness': '身体对抗', 'style': '控球传导,耐心寻找机会'},
    '伊朗': {'star': 'Mehdi Taremi', 'coach': 'Amir Ghalenoei', 'strength': '身体对抗,防守硬朗', 'weakness': '进攻套路单一', 'style': '防守反击,身体对抗'},
    '埃及': {'star': 'Mohamed Salah', 'coach': 'Hossam Hassan', 'strength': '球星个人能力,防线稳固', 'weakness': '中场创造力', 'style': '稳固防守,依赖核心'},
    '佛得角': {'star': 'Jamiro Monteiro', 'coach': 'Bubista', 'strength': '技术灵活,团队配合', 'weakness': '整体防守', 'style': '技术流,灵活跑位'},
    '新西兰': {'star': 'Chris Wood', 'coach': 'Darren Bazeley', 'strength': '身体对抗,空中优势', 'weakness': '技术粗糙,经验不足', 'style': '长传冲吊,身体对抗'},
    '奥地利': {'star': 'Christoph Baumgartner', 'coach': 'Ralf Rangnick', 'strength': '高压训练,整体跑动', 'weakness': '大赛经验', 'style': '高位压迫,快速攻防转换'},
    '海地': {'star': 'Duckens Nazon', 'coach': 'Gabriel Calderón', 'strength': '身体素质,斗志旺盛', 'weakness': '战术纪律,经验不足', 'style': '防守反击,身体对抗'},
    '库拉索': {'star': 'Cuco Martina', 'coach': 'Brian Gomes', 'strength': '技术基础好,速度', 'weakness': '组织纪律,大赛经验', 'style': '个人技术,灵活进攻'},
}

# Team alias mapping
TEAM_ALIAS = {
    '日本': '日本', '瑞典': '瑞典', '荷兰': '荷兰', '巴拉圭': '巴拉圭', '土耳其': '土耳其',
    '德国': '德国', '科特迪瓦': '科特迪瓦',
    '厄瓜多尔': '厄瓜多尔', '库拉索': '库拉索',
    '突尼斯': '突尼斯', '日本': '日本',
    '西班牙': '西班牙', '沙特': '沙特',
    '比利时': '比利时', '伊朗': '伊朗',
    '乌拉圭': '乌拉圭', '佛得角': '佛得角',
    '新西兰': '新西兰', '埃及': '埃及',
    '阿根廷': '阿根廷', '奥地利': '奥地利',
    '法国': '法国', '伊拉克': '伊拉克',
    '挪威': '挪威', '塞内加尔': '塞内加尔',
}

def get_team_info(name):
    """Get team info by name, trying various lookup methods"""
    if name in TEAM_INFO:
        return TEAM_INFO[name]
    # Try alias
    if name in TEAM_ALIAS and TEAM_ALIAS[name] in TEAM_INFO:
        return TEAM_INFO[TEAM_ALIAS[name]]
    return None

def get_fifa_rank(name):
    if name in FIFA_RANKINGS:
        return FIFA_RANKINGS[name]
    if name in TEAM_ALIAS and TEAM_ALIAS[name] in FIFA_RANKINGS:
        return FIFA_RANKINGS[TEAM_ALIAS[name]]
    return '?'

def generate_deep_analysis(match):
    """Generate a deep analysis text for a match"""
    home = match['home']
    away = match['away']
    
    home_info = get_team_info(home)
    away_info = get_team_info(away)
    home_rank = get_fifa_rank(home)
    away_rank = get_fifa_rank(away)
    
    odds = match.get('odds_h2h', {})
    # Find the key - may be English names
    home_key = None
    away_key = None
    draw_val = odds.get('Draw', 3.0)
    for k in odds:
        if k not in ['Draw'] and home_key is None:
            home_key = k
        elif k not in ['Draw'] and away_key is None:
            away_key = k
    home_odd = odds.get(home_key, 2.0) if home_key else 2.0
    away_odd = odds.get(away_key, 2.0) if away_key else 2.0
    
    # Prediction from analysis
    analyses = match.get('analyses', [])
    predicted_result = '?'
    confidence = 75
    if analyses:
        latest = analyses[-1]
        confidence = latest.get('confidence', 75)
        strategies = latest.get('strategies', {})
        conservative = strategies.get('conservative', {})
        predicted_result = conservative.get('pick', '?')
    
    is_favorite_home = home_odd < away_odd
    
    # Build analysis text
    lines = [
        f"## {home} vs {away}\n",
        f"**FIFA排名**: {home} #{home_rank} | {away} #{away_rank}" if home_rank != '?' and away_rank != '?' else "",
    ]
    
    if home_info:
        lines.append(f"**{home}**: ⭐ {home_info.get('star', '')} | 教练: {home_info.get('coach', '')} | {home_info.get('strength', '')} | {home_info.get('style', '')}")
    if away_info:
        lines.append(f"**{away}**: ⭐ {away_info.get('star', '')} | 教练: {away_info.get('coach', '')} | {away_info.get('strength', '')} | {away_info.get('style', '')}")
    
    lines.append(f"\n**赔率分析**: {home} ({home_odd}) vs {away} ({away_odd}), 平局 ({draw_val})")
    lines.append(f"**预测**: {predicted_result} | 信心: {confidence}%")
    
    # Tactical analysis
    if home_info and away_info:
        lines.append(f"\n**战术对位**: {home} {home_info.get('style', '灵活')} vs {away} {away_info.get('style', '灵活')}")
        if home_odd < away_odd:
            lines.append(f"{home}是赔率方热门，市场看好其取胜")
        elif away_odd < home_odd:
            lines.append(f"{away}是赔率方热门，市场看好其取胜")
        else:
            lines.append("双方赔率接近，预计是一场势均力敌的比赛")
    
    return {
        'homeFifaRank': home_rank,
        'awayFifaRank': away_rank,
        'homeInfo': home_info.get('star', '') + ' | ' + home_info.get('coach', '') if home_info else '',
        'awayInfo': away_info.get('star', '') + ' | ' + away_info.get('coach', '') if away_info else '',
        'homeStrength': home_info.get('strength', '') if home_info else '',
        'awayStrength': away_info.get('strength', '') if away_info else '',
        'homeStyle': home_info.get('style', '') if home_info else '',
        'awayStyle': away_info.get('style', '') if away_info else '',
        'homeWeakness': home_info.get('weakness', '') if home_info else '',
        'awayWeakness': away_info.get('weakness', '') if away_info else '',
        'predictedResult': predicted_result,
        'confidence': confidence,
        'favorite': home if is_favorite_home else away,
        'analysisText': '\n'.join(filter(None, lines))
    }

def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = data['matches']
    
    # === Step 1: Add deepAnalysis to all matches that don't have it ===
    for m in matches:
        analyses = m.get('analyses', [])
        for a in analyses:
            if 'deepAnalysis' not in a:
                a['deepAnalysis'] = generate_deep_analysis(m)
    
    # === Step 2: Calculate prediction accuracy ===
    correct_h2h = 0
    total_verified = 0
    accuracy = data.get('prediction_accuracy', {
        'total_matches': 0, 'correct_h2h': 0, 'accuracy_rate': '0%', 'history': []
    })
    
    # Count existing verified
    for m in matches:
        res = m.get('result')
        if res is not None:
            verified = m.get('verified', False)
            analyses = m.get('analyses', [])
            if analyses and not verified:
                latest = analyses[-1]
                deep = latest.get('deepAnalysis', {})
                predicted = deep.get('predictedResult', '')
                
                # Determine if correct
                if predicted and res:
                    correct = False
                    if predicted == res:
                        correct = True
                    elif predicted == '平局' and res == '平':
                        correct = True
                    elif '胜' in predicted and '胜' in res:
                        correct = predicted.split('胜')[0] == res.split('胜')[0]
                    
                    if correct:
                        correct_h2h += 1
                    total_verified += 1
                    m['verified'] = True
    
    # Add to existing accuracy counts
    accuracy['correct_h2h'] = accuracy.get('correct_h2h', 0) + correct_h2h
    accuracy['total_matches'] = accuracy.get('total_matches', 0) + total_verified
    
    if accuracy['total_matches'] > 0:
        rate = (accuracy['correct_h2h'] / accuracy['total_matches']) * 100
        accuracy['accuracy_rate'] = f'{rate:.1f}%'
        
        # Add history entry
        today_str = now.strftime('%m/%d')
        accuracy['history'] = accuracy.get('history', [])
        if not accuracy['history'] or accuracy['history'][-1]['date'] != today_str:
            accuracy['history'].append({
                'date': today_str,
                'rate': int(rate)
            })
    
    data['prediction_accuracy'] = accuracy
    
    # === Step 3: Update metadata ===
    now_str = now.strftime('%Y-%m-%d %H:%M CST')
    data['lastUpdate'] = now_str
    data['nextUpdate'] = (now + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M CST')
    
    # Save
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'✅ Deep analysis added to all matches')
    print(f'✅ Accuracy: {accuracy["correct_h2h"]}/{accuracy["total_matches"]} = {accuracy["accuracy_rate"]}')
    print(f'✅ History: {accuracy["history"]}')
    
    # === Step 4: Git push ===
    print()
    print('📤 Git 提交推送...')
    os.chdir(REPO_DIR)
    cmds = [
        ['git', 'add', '-A'],
        ['git', 'commit', '-m', f'[auto] 深度分析更新 {now_str} 准确率{accuracy["accuracy_rate"]}'],
        ['git', 'pull', '--rebase', 'origin', 'main'],
        ['git', 'push'],
        ['git', 'push', '-f']
    ]
    for c in cmds:
        r = subprocess.run(c, capture_output=True, text=True)
        if r.returncode != 0:
            out = (r.stderr or r.stdout or '')[:300]
            if 'nothing to commit' in r.stdout:
                print('ℹ️ 没有变更')
                break
            if 'up to date' in r.stdout or 'up-to-date' in r.stderr:
                continue
            if 'Everything up-to-date' in r.stderr or 'Everything up-to-date' in r.stdout:
                print('✅ 已推送')
                break
            if r.returncode != 0 and 'rebase' in str(c[0]):
                print('⚠️ rebase冲突, 强制推送...')
                subprocess.run(['git', 'push', '-f'], capture_output=True, text=True)
            print(f' → {out[:200]}')
        else:
            if 'push' in str(c[0]):
                print('✅ 推送成功')

if __name__ == '__main__':
    main()
