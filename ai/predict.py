from pathlib import Path
import joblib,pandas as pd
MODEL_PATH=Path(__file__).resolve().parent.parent/'ai_model'/'irrigation_rf.joblib'
FEATURES=['temperature','humidity','rain','wind_speed','soil_moisture']
_model=None
if MODEL_PATH.exists():
    try: _model=joblib.load(MODEL_PATH)
    except Exception: pass
def predict_irrigation(v):
    if _model is None: return {'irrigation':v['soil_moisture']<30 and v.get('rain',0)<1,'confidence':None,'model':'simulation_fallback','message':'Chưa có model Random Forest; đang dùng rule mô phỏng. Chạy python -m ai.train <dataset.csv> để tạo model.'}
    x=pd.DataFrame([[v.get(f,0) for f in FEATURES]],columns=FEATURES); pred=int(_model.predict(x)[0]); conf=float(max(_model.predict_proba(x)[0])) if hasattr(_model,'predict_proba') else None
    return {'irrigation':bool(pred),'confidence':conf,'model':'random_forest'}
