import json
from datetime import datetime

with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('matches', [])

predicted_home_away_map = {}

analysis_time = "2026-06-21 00:38"

def calc_jingcai(euro_odds):
    """Euro odds to 竞彩 odds: max(1.00, 1 - (1-euro)*0.69)"""
    return round(max(1.0, 1 - (1 - euro_odds) * 0.69), 2)

def determine_prediction(odds_h2h, home_name, away_name):
    """Determine predicted winner based on odds"""
    # Get the three outcomes
    home_odds = odds_h2h.get(home_name, odds_h2h.get(list(odds_h2h.keys())[0], 2.0))
    draw_odds = odds_h2h.get('Draw', 3.5)
    away_odds = odds_h2h.get(away_name, odds_h2h.get(list(odds_h2h.keys())[2], 3.0))
    
    # Calculate implied probabilities
    home_prob = 1/home_odds
    draw_prob = 1/draw_odds
    away_prob = 1/away_odds
    total = home_prob + draw_prob + away_prob
    home_prob_norm = home_prob / total * 100
    draw_prob_norm = draw_prob / total * 100
    away_prob_norm = away_prob / total * 100
    
    # Determine pick
    if home_prob_norm >= 50:
        pick = f"{home_name}胜"
        predicted = home_name
        confidence = int(min(home_prob_norm, 85))
    elif away_prob_norm >= 45:
        pick = f"{away_name}胜"
        predicted = away_name
        confidence = int(min(away_prob_norm, 80))
    else:
        pick = "平局"
        predicted = "平"
        confidence = int(min(draw_prob_norm, 60))
    
    return pick, predicted, confidence, home_prob_norm, draw_prob_norm, away_prob_norm, home_odds, draw_odds, away_odds

def generate_report(home, away, pick, predicted, confidence, home_prob, draw_prob, away_prob, 
                    home_odds, draw_odds, away_odds, goal_count):
    """Generate fullReport HTML"""
    jc_home = calc_jingcai(home_odds)
    jc_draw = calc_jingcai(draw_odds)
    jc_away = calc_jingcai(away_odds)
    
    report = f"""
    <div style="font-family: sans-serif; max-width: 640px;">
    <div style="text-align:center;padding:12px;background:linear-gradient(135deg,#1a1040,#0c0a1a);border-radius:12px;margin-bottom:12px;border:1px solid rgba(255,215,0,.2);">
      <div style="font-size:20px;font-weight:700;color:#ffd700;">🎯 预测：{pick}</div>
      <div style="font-size:13px;color:#e8e0f0;margin:4px 0;">{home} vs {away}</div>
      <div style="font-size:11px;color:#7a7090;">信心 ★{'★' * (confidence//20)}☆{'☆' * (5 - confidence//20)} | {confidence}%</div>
    </div>
    
    <div style="margin:8px 0;">
      <div style="display:flex;justify-content:space-between;padding:6px 10px;background:rgba(255,215,0,.03);border-radius:6px;margin:2px 0;">
        <span style="color:#7a7090;">{home}概率</span>
        <span style="color:#ffd700;font-weight:700;">{home_prob:.1f}%</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:6px 10px;background:rgba(255,215,0,.03);border-radius:6px;margin:2px 0;">
        <span style="color:#7a7090;">平局概率</span>
        <span style="color:#7a7090;font-weight:700;">{draw_prob:.1f}%</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:6px 10px;background:rgba(255,215,0,.03);border-radius:6px;margin:2px 0;">
        <span style="color:#7a7090;">{away}概率</span>
        <span style="color:#7a7090;font-weight:700;">{away_prob:.1f}%</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:6px 10px;background:rgba(255,215,0,.03);border-radius:6px;margin:2px 0;">
        <span style="color:#7a7090;">预计进球</span>
        <span style="color:#66d4aa;font-weight:700;">{goal_count}球</span>
      </div>
    </div>
    
    <hr style="border:none;border-top:1px solid rgba(255,215,0,.1);margin:10px 0;">
    
    <div style="font-size:12px;color:#e8e0f0;margin:8px 0;">
      <div style="color:#ffd700;font-size:13px;font-weight:700;margin-bottom:6px;">💶 赔率对比</div>
      <table style="width:100%;border-collapse:collapse;">
        <tr style="border-bottom:1px solid rgba(255,215,0,.1);">
          <td style="padding:4px 8px;color:#7a7090;">选项</td>
          <td style="padding:4px 8px;color:#7a7090;">欧洲赔率</td>
          <td style="padding:4px 8px;color:#7a7090;">竞彩赔率</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,215,0,.05);">
          <td style="padding:4px 8px;color:#{'#00d4aa' if predicted == home else ''};font-weight:{'700' if predicted == home else ''};">{home}</td>
          <td style="padding:4px 8px;color:#{'#00d4aa' if predicted == home else ''};font-weight:{'700' if predicted == home else ''};">{home_odds}</td>
          <td style="padding:4px 8px;color:#{'#00d4aa' if predicted == home else ''};font-weight:{'700' if predicted == home else ''};">{jc_home}</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,215,0,.05);">
          <td style="padding:4px 8px;color:{'#00d4aa' if predicted == '平' else ''};">平局</td>
          <td style="padding:4px 8px;color:{'#00d4aa' if predicted == '平' else ''};">{draw_odds}</td>
          <td style="padding:4px 8px;color:{'#00d4aa' if predicted == '平' else ''};">{jc_draw}</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,215,0,.05);">
          <td style="padding:4px 8px;color:{'#00d4aa' if predicted == away else ''};">{away}</td>
          <td style="padding:4px 8px;color:{'#00d4aa' if predicted == away else ''};">{away_odds}</td>
          <td style="padding:4px 8px;color:{'#00d4aa' if predicted == away else ''};">{jc_away}</td>
        </tr>
      </table>
    </div>
    
    <hr style="border:none;border-top:1px solid rgba(255,215,0,.1);margin:10px 0;">
    
    <div style="background:rgba(255,215,0,.02);border-left:3px solid #00d4aa;border-radius:0 6px 6px 0;padding:8px 10px;margin:6px 0;">
      <div style="font-size:11px;font-weight:700;color:#00d4aa;">🛡️ 保守策略</div>
      <div style="font-size:12px;color:#e8e0f0;margin:2px 0;">🎯 {pick} <span style="color:#{'#00d4aa' if predicted != '平' else '#ffd700'};">@{home_odds if predicted == home else (draw_odds if predicted == '平' else away_odds)}</span></div>
      <div style="font-size:10px;color:#7a7090;">💰 每100元 → ¥{round(100 * (home_odds if predicted == home else (draw_odds if predicted == '平' else away_odds)))}  |  单关</div>
    </div>
    
    <div style="background:rgba(255,215,0,.02);border-left:3px solid #ffd700;border-radius:0 6px 6px 0;padding:8px 10px;margin:6px 0;">
      <div style="font-size:11px;font-weight:700;color:#ffd700;">⚡ 均衡策略</div>
      <div style="font-size:12px;color:#e8e0f0;margin:2px 0;">🎯 {pick} @ {jc_home if predicted == home else (jc_draw if predicted == '平' else jc_away)}</div>
      <div style="font-size:10px;color:#7a7090;">💰 每100元 → ¥{round(100 * (jc_home if predicted == home else (jc_draw if predicted == '平' else jc_away)))}  |  竞彩</div>
    </div>
    
    <div style="background:rgba(255,215,0,.02);border-left:3px solid #ff4757;border-radius:0 6px 6px 0;padding:8px 10px;margin:6px 0;">
      <div style="font-size:11px;font-weight:700;color:#ff4757;">🔥 激进策略</div>
      <div style="font-size:12px;color:#e8e0f0;margin:2px 0;">🎯 进球数 Over 2.5 <span style="color:#ff4757;">@1.85</span></div>
      <div style="font-size:10px;color:#7a7090;">💰 每100元 → ¥185  |  大小球</div>
    </div>
    
    <hr style="border:none;border-top:1px solid rgba(255,215,0,.1);margin:10px 0;">
    <div style="font-size:10px;color:#7a7090;text-align:center;">
      生成于 {analysis_time}  |  ⚠️ 仅供参考，理性投注
    </div>
    </div>
    """
    return report

def update_match_analysis(m, idx):
    """Update a match's latest analysis with deepAnalysis and proper strategies"""
    home = m.get('home', '')
    away = m.get('away', '')
    odds_h2h = m.get('odds_h2h', {})
    
    if not odds_h2h:
        print(f"  ⚠️ {home} vs {away}: no odds_h2h, skipping")
        return False
    
    # Get the latest analysis
    analyses = m.get('analyses', [])
    if not analyses:
        print(f"  ⚠️ {home} vs {away}: no analyses, skipping")
        return False
    
    last = analyses[-1]
    
    # Determine prediction
    pick, predicted, confidence, home_prob, draw_prob, away_prob, home_odds, draw_odds, away_odds = \
        determine_prediction(odds_h2h, home, away)
    
    # Get goal count from existing analysis
    goal_count = last.get('goalCount', 2)
    
    # Add deepAnalysis
    last['deepAnalysis'] = {
        'predictedResult': pick,
        'predictedWinner': predicted,
        'confidence': confidence,
        'homeProb': round(home_prob, 1),
        'drawProb': round(draw_prob, 1),
        'awayProb': round(away_prob, 1),
        'homeOdds': home_odds,
        'drawOdds': draw_odds,
        'awayOdds': away_odds,
        'analysisTime': analysis_time
    }
    
    # Fix strategies - pick field should only have result name, no odds
    strategies = last.get('strategies', {})
    if strategies:
        # Conservative - should be fine already
        if 'conservative' in strategies:
            strategies['conservative']['pick'] = pick
        
        # Balanced - remove odds from pick
        if 'balanced' in strategies:
            strategies['balanced']['pick'] = pick
        
        # Aggressive
        if 'aggressive' in strategies:
            strategies['aggressive']['pick'] = f"总进球 Over 2.5"
    
    # Update jingcai_all
    jc_all = last.get('jingcai_all', {})
    if 'spf' in jc_all:
        jc_all['spf'][home] = calc_jingcai(home_odds)
        jc_all['spf']['Draw'] = calc_jingcai(draw_odds)
        jc_all['spf'][away] = calc_jingcai(away_odds)
    
    # Regenerate fullReport
    last['fullReport'] = generate_report(home, away, pick, predicted, confidence, 
                                          home_prob, draw_prob, away_prob,
                                          home_odds, draw_odds, away_odds, goal_count)
    
    print(f"  ✅ {home} vs {away}: {pick} ({confidence}%)")
    return True

print("🔮 轻量模式分析中...")
print(f"比赛总数: {len(matches)}")
print()

updated = 0
for i, m in enumerate(matches):
    if update_match_analysis(m, i):
        updated += 1

print(f"\n✅ 更新了 {updated}/{len(matches)} 场比赛")

# Save back
with open(r'C:\Users\19916\Desktop\xj-local\worldcup\data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("💾 data.json 已保存")
