#!/usr/bin/env python3
"""Coleta diária de precipitação recente estimada e previsão Open-Meteo; não são observações oficiais INMET."""
import json,urllib.request,urllib.parse
from datetime import date,datetime,timedelta,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data/latest.json"
REGIONS=[{"regiao":"Médio-Norte · Sorriso","lat":-12.54,"lon":-55.72},{"regiao":"Oeste · Campo Novo do Parecis","lat":-13.66,"lon":-57.89},{"regiao":"Norte · Sinop","lat":-11.86,"lon":-55.51},{"regiao":"Centro-Sul · Cuiabá","lat":-15.60,"lon":-56.10},{"regiao":"Noroeste · Juína","lat":-11.42,"lon":-58.76},{"regiao":"Nordeste · Canarana","lat":-13.55,"lon":-52.27},{"regiao":"Sudeste · Primavera do Leste","lat":-15.56,"lon":-54.30}]
def get_json(url):
 req=urllib.request.Request(url,headers={"User-Agent":"PainelSafraMT/1.0"})
 with urllib.request.urlopen(req,timeout=25) as r:return json.loads(r.read().decode())
def point(r):
 today=date.today();start=today-timedelta(days=7)
 def query(base,params):return get_json(base+"?"+urllib.parse.urlencode(params))
 obs=fc=None;errs=[]
 try:
  a=query("https://archive-api.open-meteo.com/v1/archive",{"latitude":r["lat"],"longitude":r["lon"],"start_date":start.isoformat(),"end_date":(today-timedelta(days=1)).isoformat(),"daily":"precipitation_sum","timezone":"America/Cuiaba"})
  vals=[v for v in (a.get("daily",{}).get("precipitation_sum") or []) if isinstance(v,(int,float))]
  if vals:obs=round(sum(vals),1)
 except Exception as e:errs.append("arquivo: "+str(e)[:100])
 try:
  f=query("https://api.open-meteo.com/v1/forecast",{"latitude":r["lat"],"longitude":r["lon"],"forecast_days":7,"daily":"precipitation_sum","timezone":"America/Cuiaba"})
  vals=[v for v in (f.get("daily",{}).get("precipitation_sum") or []) if isinstance(v,(int,float))]
  if vals:fc=round(sum(vals),1)
 except Exception as e:errs.append("previsão: "+str(e)[:100])
 return {"regiao":r["regiao"],"chuva_observada_7d_mm":obs,"previsao_7d_mm":fc,"atualizado_em":today.isoformat(),"fonte":"Open-Meteo (arquivo/reanálise e modelo; não é observação oficial INMET)","latitude":r["lat"],"longitude":r["lon"],"avisos":errs}
def main():
 payload=json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"plantio":{},"meteorologia":{},"historico_plantio":[],"status":{}}
 today=date.today().isoformat();old={x.get("regiao"):x for x in payload.get("meteorologia",{}).get("regioes",[])};results=[]
 for r in REGIONS:
  try:
   x=point(r)
   if x["chuva_observada_7d_mm"] is None and x["previsao_7d_mm"] is None and r["regiao"] in old:x=old[r["regiao"]];x["aviso"]="Falha na atualização; preservado último valor válido."
   results.append(x)
  except Exception as e:
   x=old.get(r["regiao"],{"regiao":r["regiao"],"chuva_observada_7d_mm":None,"previsao_7d_mm":None,"atualizado_em":today,"fonte":"Sem dado válido"});x["aviso"]="Falha na coleta: "+str(e)[:120];results.append(x)
 payload["meteorologia"]={"atualizado_em":today,"observacao":"Precipitação recente estimada por arquivo/reanálise e previsão por modelo Open-Meteo. Não é medição oficial INMET e ponto não representa toda a macrorregião.","regioes":results}
 payload.setdefault("status",{})["ultima_execucao"]=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
 ok=any(x.get("previsao_7d_mm") is not None or x.get("chuva_observada_7d_mm") is not None for x in results)
 payload["status"]["meteorologia"]="OK" if ok else "Falha; dados anteriores preservados quando disponíveis"
 payload["status"].setdefault("plantio","Pendente de validação manual com boletim oficial do IMEA");payload["status"].setdefault("avisos",[])
 OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8");print("Regiões processadas:",len(results))
if __name__=="__main__":main()
