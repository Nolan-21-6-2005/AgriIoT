from pathlib import Path
import sys,joblib,pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
if len(sys.argv)<2: raise SystemExit('python -m ai.train <csv>')
df=pd.read_csv(sys.argv[1]); features=['temperature','humidity','rain','wind_speed','soil_moisture']; missing=[x for x in features+['irrigation'] if x not in df]
if missing: raise SystemExit(f'Thiếu cột: {missing}')
X=df[features].fillna(0); y=df['irrigation'].astype(int); Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
m=RandomForestClassifier(n_estimators=200,random_state=42,class_weight='balanced'); m.fit(Xtr,ytr); out=Path(__file__).resolve().parent.parent/'ai_model'/'irrigation_rf.joblib'; joblib.dump(m,out); print(out)
