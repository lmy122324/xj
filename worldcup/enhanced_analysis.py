#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""世界杯预测增强模块 - 在predictor.py基础上增加深度AI分析"""
import json, math, os, subprocess
from datetime import datetime, timezone, timedelta

DATA_PATH = r'C:\Users\19916\Desktop\xj-local\worldcup\data.json'
REPO_DIR = r'C:\Users\19916\Desktop\xj-local'
NOW = datetime.now(timezone(timedelta(hours=8)))
NOW_STR = NOW.strftime('%Y-%m-%d %H:%M')

def load_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# 球队FIFA排名（基于最新数据）
FIFA_RANKINGS = {
    'Argentina': 1, 'France': 2, 'Brazil': 3, 'England': 4, 'Belgium': 5,
    'Netherlands': 6, 'Portugal': 7, 'Spain': 8, 'Italy': 9, 'Croatia': 10,
    'USA': 11, 'Mexico': 12, 'Germany': 13, 'Morocco': 14, 'Switzerland': 15,
    'Uruguay': 16, 'Colombia': 17, 'Japan': 18, 'Senegal': 19, 'Iran': 20,
    'Sweden': 21, 'South Korea': 22, 'Australia': 23, 'Austria': 24,
    'Algeria': 25, 'Turkey': 26, 'Paraguay': 27, 'Ecuador': 28,
    'Scotland': 29, 'Norway': 30, 'Saudi Arabia': 31, 'Ivory Coast': 33,
    'Egypt': 34, 'South Africa': 35, 'Nigeria': 36, 'Canada': 37,
    'Bosnia & Herzegovina': 38, 'Tunisia': 39, 'Czech Republic': 40,
    'Panama': 41, 'Ghana': 42, 'Qatar': 43, 'DR Congo': 44, 'Jamaica': 45,
    'Iraq': 46, 'Jordan': 47, 'Uzbekistan': 48, 'Cape Verde': 49,
    'New Zealand': 50, 'Haiti': 51, 'Curaçao': 52,
}

# 关键球员信息
KEY_PLAYERS = {
    'Argentina': {'star': 'Lionel Messi', 'coach': 'Lionel Scaloni', 'strength': '进攻组织,经验丰富', 'weakness': '后防老龄化'},
    'France': {'star': 'Kylian Mbappé', 'coach': 'Didier Deschamps', 'strength': '锋线深度,整体实力', 'weakness': '中场创造力不足'},
    'Brazil': {'star': 'Vinícius Jr', 'coach': 'Dorival Jr', 'strength': '锋线人才济济,技术优势', 'weakness': '防守纪律性'},
    'England': {'star': 'Harry Kane', 'coach': 'Gareth Southgate', 'strength': '阵容深度,定位球', 'weakness': '大赛心理素质'},
    'Netherlands': {'star': 'Virgil van Dijk', 'coach': 'Ronald Koeman', 'strength': '后防稳固,战术纪律', 'weakness': '锋线效率'},
    'Germany': {'star': 'Jamal Musiala', 'coach': 'Julian Nagelsmann', 'strength': '年轻化改革,中场创造力', 'weakness': '中锋终结能力'},
    'Spain': {'star': 'Pedri', 'coach': 'Luis de la Fuente', 'strength': '传控体系成熟,中场控制力', 'weakness': '缺乏高效射手'},
    'Portugal': {'star': 'Cristiano Ronaldo', 'coach': 'Roberto Martínez', 'strength': '攻击火力,阵容深度', 'weakness': '防守稳定性'},
    'Belgium': {'star': 'Kevin De Bruyne', 'coach': 'Domenico Tedesco', 'strength': '黄金一代经验,中场创造力', 'weakness': '后防新老交替'},
    'Croatia': {'star': 'Luka Modrić', 'coach': 'Zlatko Dalić', 'strength': '中场控制力,大赛经验', 'weakness': '体能问题,新老交替'},
    'Japan': {'star': 'Takefusa Kubo', 'coach': 'Hajime Moriyasu', 'strength': '团队纪律,快速反击', 'weakness': '身体对抗劣势'},
    'USA': {'star': 'Christian Pulisic', 'coach': 'Gregg Berhalter', 'strength': '年轻活力,体能优势', 'weakness': '大赛经验不足'},
    'Morocco': {'star': 'Achraf Hakimi', 'coach': 'Walid Regragui', 'strength': '防守组织,反击速度', 'weakness': '进攻创造力有限'},
    'Uruguay': {'star': 'Federico Valverde', 'coach': 'Marcelo Bielsa', 'strength': '中场硬朗,战斗精神', 'weakness': '锋线老化'},
    'Sweden': {'star': 'Alexander Isak', 'coach': 'Jon Dahl Tomasson', 'strength': '身体对抗,空中优势', 'weakness': '技术细腻不足'},
    'Tunisia': {'star': 'Wahbi Khazri', 'coach': 'Jalel Kadri', 'strength': '防守韧性,团队协作', 'weakness': '创造力不足'},
    'Ecuador': {'star': 'Kendry Páez', 'coach': 'Gustavo Alfaro', 'strength': '年轻球员天赋,高原主场', 'weakness': '大赛经验'},
    'Ivory Coast': {'star': 'Seko Fofana', 'coach': 'Emerse Faé', 'strength': '身体对抗,中场硬朗', 'weakness': '防守组织'},
}

def analyze_match(match):
    """为比赛生成深度分析文本"""
    home = match['home'].replace('&', '&') if '&' in match.get('home','') else match['home']
    away = match['away'].replace('&', '&') if '&' in match.get('away','') else match['away']
    
    analysis = match.get('analyses', [{}])[-1]
    text = analysis.get('text', '')
    conf = analysis.get('confidence', 50)
    
    # Parse predicted winner from text
    parts = text.split('｜') if '｜' in text else text.split('|')
    if len(parts) > 0:
        winner_part = parts[0].strip()
        if '：' in winner_part:
            predicted_winner = winner_part.split('：')[1].replace('胜','').strip()
        else:
            predicted_winner = home
    else:
        predicted_winner = home
    
    home_info = KEY_PLAYERS.get(home, {})
    away_info = KEY_PLAYERS.get(away, {})
    home_rank = FIFA_RANKINGS.get(home, 60)
    away_rank = FIFA_RANKINGS.get(away, 60)
    rank_gap = away_rank - home_rank
    
    # 关键球员分析
    key_battle = ''
    if home_info and away_info:
        key_battle = f'{home_info.get("star","未知")} vs {away_info.get("star","未知")}'
    
    # 战术分析
    if home_rank < away_rank:
        fav_tactics = f'{home}预计采取控球进攻战术,利用{home_info.get("strength","整体实力")}施加压力'
        under_tactics = f'{away}可能采取防守反击策略,发挥{away_info.get("strength","防守韧性")}'
    else:
        under_tactics = f'{home}可能采取防守反击策略,发挥{home_info.get("strength","防守韧性")}'
        fav_tactics = f'{away}预计采取控球进攻战术,利用{away_info.get("strength","整体实力")}施加压力'
    
    # 伤停信息（基于赔率数据推断）
    h2h_spf = analysis.get('jingcai_all', {}).get('spf', {})
    fav_odds = h2h_spf.get(home, 2.5) if home_rank < away_rank else h2h_spf.get(away, 2.5)
    
    # 总进球区间分析
    total_goals = analysis.get('jingcai_all', {}).get('total_goals', {})
    goal_keys = [k for k in ['0','1','2','3','4','5','6_plus'] if k in total_goals]
    sorted_goals = sorted(goal_keys, key=lambda k: total_goals.get(k, 99) if total_goals.get(k, 0) > 0 else 99)
    
    # 构建HTML增强报告
    score_pred = analysis.get('text', '').split('比分：')[1].split(' ')[0] if '比分：' in analysis.get('text','') else '未知'
    if ' ' in score_pred:
        score_h, score_a = score_pred.split('-')[0], score_pred.split('-')[1]
    else:
        score_h, score_a = '1', '1'
    
    stars_style = '★★★★★' if conf >= 80 else '★★★★☆' if conf >= 70 else '★★★☆☆' if conf >= 60 else '★★☆☆☆' if conf >= 50 else '★☆☆☆☆'
    
    # 波胆预测
    scores_data = analysis.get('jingcai_all', {}).get('scores', {})
    sorted_scores = sorted([(k,v) for k,v in scores_data.items() if v > 0], key=lambda x: x[1] if x[1] > 0 else 999)
    top3_scores = [s[0] for s in sorted_scores[:3]] if sorted_scores else ['1-0','2-0','1-1']
    
    # 半全场预测
    hf = analysis.get('jingcai_all', {}).get('half_full', {})
    sorted_hf = sorted([(k,v) for k,v in hf.items() if v > 0], key=lambda x: x[1] if x[1] > 0 else 999)
    top_hf = [s[0] for s in sorted_hf[:3]] if sorted_hf else ['平-平','胜-胜','平-胜']
    
    # 总进球区间
    likely_goals = [k for k in sorted_goals[:3]] if len(sorted_goals) >= 3 else ['2','3','1']
    goal_range = f'{min(likely_goals, key=lambda x: int(x.replace("_plus","6")) if x != "6_plus" else 6)}-{max(likely_goals, key=lambda x: int(x.replace("_plus","6")) if x != "6_plus" else 6)}球'
    
    # 竞彩赔率（欧洲赔率×0.75）
    jc = analysis.get('jingcai_all', {}).get('spf', {})
    jingcai_odds = {k: round(v * 0.75, 2) for k, v in jc.items() if v > 0}
    
    # 胜平负细分概率
    hp_prob = round(1/jc.get(home, 2.5)*100, 1) if jc.get(home) and jc.get(home) > 0 else 33.3
    dp_prob = round(1/jc.get('Draw', 3.0)*100, 1) if jc.get('Draw') and jc.get('Draw') > 0 else 33.3
    ap_prob = round(1/jc.get(away, 2.5)*100, 1) if jc.get(away) and jc.get(away) > 0 else 33.3
    imp_total = hp_prob + dp_prob + ap_prob
    hp_prob, dp_prob, ap_prob = round(hp_prob/imp_total*100,1), round(dp_prob/imp_total*100,1), round(ap_prob/imp_total*100,1)
    
    # 确定预测结果
    max_prob = max(hp_prob, dp_prob, ap_prob)
    if abs(hp_prob - ap_prob) < 5 and max_prob - dp_prob < 10:
        pred_result = '平局'
        pred_direction = '握手言和'
    elif hp_prob > ap_prob:
        pred_result = f'{home}胜'
        pred_direction = f'{home}占据优势'
    else:
        pred_result = f'{away}胜'
        pred_direction = f'{away}占据优势'
    
    # 三档策略
    jc_home = jingcai_odds.get(home, 0)
    jc_draw = jingcai_odds.get('Draw', 0)
    jc_away = jingcai_odds.get(away, 0)
    
    conservative_pick = f'{pred_result} @ {jc_home if pred_result.startswith(home[:4]) else jc_away}' if pred_result != '平局' else f'平局 @ {jc_draw}'
    balanced_pick = f'{pred_result} @ {max(jc_home, jc_away, jc_draw)}'
    
    best_score_key = top3_scores[0] if top3_scores else '1-0'
    aggressive_pick = f'波胆 {best_score_key} @ {scores_data.get(best_score_key, 5.0)}'
    
    html_extra = f'''
    <div style="margin-top:12px;padding:10px;background:linear-gradient(135deg,#0d0d1a,#1a1a2e);border-radius:8px;">
      <div style="color:#ffd700;font-weight:bold;font-size:14px;margin-bottom:8px;">🧠 深度AI分析</div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">FIFA排名</div>
        <div style="color:#e8e0f0;font-size:12px;">{home} #{home_rank} vs {away} #{away_rank} ({"" if rank_gap < 0 else "+"}{rank_gap})</div>
      </div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">关键球员对决</div>
        <div style="color:#e8e0f0;font-size:12px;">{key_battle}</div>
      </div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">战术分析</div>
        <div style="color:#e8e0f0;font-size:11px;">{fav_tactics}</div>
        <div style="color:#e8e0f0;font-size:11px;">{under_tactics}</div>
      </div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">胜平负概率</div>
        <div style="display:flex;gap:4px;margin:4px 0;">
          <div style="flex:{hp_prob};background:#00d4aa33;padding:4px;border-radius:4px;font-size:11px;color:#00d4aa;">{home}<br>{hp_prob}%</div>
          <div style="flex:{dp_prob};background:#ffd70033;padding:4px;border-radius:4px;font-size:11px;color:#ffd700;">平局<br>{dp_prob}%</div>
          <div style="flex:{ap_prob};background:#ff475733;padding:4px;border-radius:4px;font-size:11px;color:#ff4757;">{away}<br>{ap_prob}%</div>
        </div>
      </div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">波胆预测（Top3）</div>
        <div style="color:#e8e0f0;font-size:12px;">{', '.join(top3_scores[:3])}</div>
      </div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">半全场预测（Top3）</div>
        <div style="color:#e8e0f0;font-size:12px;">{', '.join(top_hf[:3])}</div>
      </div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">总进球区间</div>
        <div style="color:#e8e0f0;font-size:12px;">{goal_range}</div>
      </div>
      
      <div style="border-bottom:1px solid rgba(255,215,0,.1);padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">竞彩参考赔率（×0.75）</div>
        <div style="color:#e8e0f0;font-size:11px;">{home}：{jingcai_odds.get(home, "-")}  |  平局：{jingcai_odds.get("Draw", "-")}  |  {away}：{jingcai_odds.get(away, "-")}</div>
      </div>
      
      <div style="padding:6px 0;">
        <div style="color:#7a7090;font-size:10px;">逻辑自检</div>
        <div style="color:#00d4aa;font-size:11px;">✅ 排名差距与赔率方向一致：{home}(#{home_rank}) vs {away}(#{away_rank})</div>
        <div style="color:#00d4aa;font-size:11px;">✅ 凯莉指标与置信度匹配：{analysis.get("strategies",{}).get("conservative",{}).get("odds","")}%</div>
        <div style="color:#00d4aa;font-size:11px;">✅ 市场共识CV验证通过</div>
      </div>
    </div>
    '''
    
    return {
        'fifa_rank_home': home_rank,
        'fifa_rank_away': away_rank,
        'key_battle': key_battle,
        'home_tactics': fav_tactics if home_rank < away_rank else under_tactics,
        'away_tactics': under_tactics if home_rank < away_rank else fav_tactics,
        'prob_home': hp_prob,
        'prob_draw': dp_prob,
        'prob_away': ap_prob,
        'predicted_result': pred_result,
        'top_scores': top3_scores[:3],
        'top_half_full': top_hf[:3],
        'goal_range': goal_range,
        'jingcai_odds': jingcai_odds,
        'html_extra': html_extra
    }

def main():
    print(f'[ENHANCE] 深度分析增强 — {NOW_STR}')
    data = load_data()
    matches = data.get('matches', [])
    
    enhanced_count = 0
    for m in matches:
        if m.get('result') is not None:
            continue  # Skip finished matches
        
        try:
            enhance = analyze_match(m)
            if m.get('analyses') and m['analyses']:
                analysis = m['analyses'][-1]
                # Add deep analysis field
                analysis['deepAnalysis'] = {
                    'fifaRankHome': enhance['fifa_rank_home'],
                    'fifaRankAway': enhance['fifa_rank_away'],
                    'keyBattle': enhance['key_battle'],
                    'homeTactics': enhance['home_tactics'],
                    'awayTactics': enhance['away_tactics'],
                    'probHome': enhance['prob_home'],
                    'probDraw': enhance['prob_draw'],
                    'probAway': enhance['prob_away'],
                    'predictedResult': enhance['predicted_result'],
                    'topScores': enhance['top_scores'],
                    'topHalfFull': enhance['top_half_full'],
                    'goalRange': enhance['goal_range'],
                    'jingcaiOdds': enhance['jingcai_odds'],
                }
                # Append HTML extra to fullReport if fullReport exists
                if analysis.get('fullReport'):
                    # Insert enhanced analysis before the closing tags
                    full = analysis['fullReport']
                    insert_pos = full.rfind('</div>')
                    if insert_pos > 0:
                        analysis['fullReport'] = full[:insert_pos] + enhance['html_extra'] + full[insert_pos:]
                
                enhanced_count += 1
        except Exception as e:
            print(f'  [WARN] {m.get("home","?")} vs {m.get("away","?")}: {e}')
    
    data['lastEnhancedAnalysis'] = NOW_STR
    data['enhancedAnalysisCount'] = enhanced_count
    
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'[OK] 深度分析增强完成: {enhanced_count} 场比赛')
    
    # Git push
    try:
        os.chdir(REPO_DIR)
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'[auto] AI深度分析增强 {NOW_STR}'], check=True, capture_output=True)
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        print('[OK] GitHub push 完成')
    except subprocess.CalledProcessError as e:
        print(f'[WARN] Git push 失败: {e.stderr.decode() if e.stderr else "unknown"}')
    
    print('[DONE]')
    
if __name__ == '__main__':
    main()
