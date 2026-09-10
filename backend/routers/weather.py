from fastapi import APIRouter,HTTPException
import requests
from utils.config import HANOI
router=APIRouter(); URL='https://api.open-meteo.com/v1/forecast'
@router.get('/forecast')
def forecast():
    params={'latitude':HANOI['latitude'],'longitude':HANOI['longitude'],'current':'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code','hourly':'temperature_2m,relative_humidity_2m,precipitation_probability,weather_code','timezone':HANOI['timezone'],'forecast_days':7}
    try: data=requests.get(URL,params=params,timeout=10); data.raise_for_status(); data=data.json()
    except requests.RequestException as e: raise HTTPException(502,f'Không lấy được dữ liệu Open-Meteo: {e}')
    h=data.get('hourly',{})
    return {'location':HANOI['name'],'latitude':data.get('latitude'),'longitude':data.get('longitude'),'current':data.get('current',{}),'hourly_forecast':{'time':h.get('time',[]),'temperature':h.get('temperature_2m',[]),'humidity':h.get('relative_humidity_2m',[]),'rain_prob':h.get('precipitation_probability',[]),'weather_code':h.get('weather_code',[])}}
