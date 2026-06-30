from flask import Flask, request, jsonify
import pandas as pd
import pandas_ta as ta

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # استقبال بيانات الأسعار من منصة التداول (مثل TradingView)
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # استخراج أسعار الإغلاق
    closes = data.get('closes', [])
    
    if len(closes) < 14:
        return jsonify({"error": "Insufficient data for indicators (need at least 14 candles)"}), 400

    # تحويل البيانات وحساب مؤشر RSI
    df = pd.DataFrame({'close': closes})
    df['rsi'] = ta.rsi(df['close'], length=14)
    
    # أخذ القيمة الأخيرة للمؤشر
    current_rsi = df['rsi'].iloc[-1]
    
    # تحديد الإشارة بناءً على مستويات التشبع
    signal = "HOLD"
    if current_rsi < 30:
        signal = "BUY (Oversold)"
    elif current_rsi > 70:
        signal = "SELL (Overbought)"

    # إرجاع النتيجة
    return jsonify({
        "status": "success",
        "rsi": float(current_rsi),
        "signal": signal
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
