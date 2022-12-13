# ----  importo librerie per i grafici ----
import pandas
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import date as dt
from datetime import date as dt, timedelta
import dash_daq as daq
import numpy as np
import dash_pivottable
from dash import html



# ------- questi servono per il google sheet -----
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# ------- collego il google sheet ---------
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("YOUR GOOGLE SHEET NAME FILE").sheet1  
# ----- check del database --------------

data = sheet.get_all_records()
df = pd.DataFrame(data)


# ---- cambio le colonne in numeri -------

df['anno'] = pd.to_datetime(df['anno']) # la colonna anno mi serve che sia una data
df['mq'] = pd.to_numeric(df['mq']) #la colonna area mi serve che sia un numero per fare le somme
df['soldi'] = pd.to_numeric(df['soldi']) #costo mi serve che sia numero per sommare
df['iva'] = pd.to_numeric(df['iva']) #mi serve che sia numero per sommare
# la colonna tipologia diversifica tra consuntivo e preventivo

#pprint(data)
df.info()

# ---- qui ho sommato preventivo e consuntivo e ho i valori per fare il grafico ------

BTS = df.loc[df['tipologia'] == 'Consuntivo', 'iva'].sum() #budget totale speso, sommo la colonna ivato se è consuntivo
BTP = df.loc[df['tipologia'] == 'Preventivo', 'iva'].sum() #budget totale speso, sommo la colonna ivato se è preventivo

dfb = pd.DataFrame({'CATEGORY' : ['BUDGET'],
                    'PREVENTIVO' : [BTP],
                    'CONSUNTIVO' : [BTS],
                    })
pprint(dfb)

# ---- ora provo a tirare fuori il totale di civil works, design, ecc.. diviso tra preventivo e consuntivo

CIVIL = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'LAVORI'), 'iva'].sum()
pprint(CIVIL)
CIVILP = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'LAVORI'), 'iva'].sum()
pprint(CIVILP)

DESIGN = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'DESIGN'), 'iva'].sum()
pprint(DESIGN)
DESIGNP = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'DESIGN'), 'iva'].sum()
pprint(DESIGNP)

IT = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'IT'), 'iva'].sum()
pprint(IT)
ITP = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'IT'), 'iva'].sum()
pprint(ITP)

EM = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'EM'), 'iva'].sum()
pprint(EM)
EMP = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'EM'), 'iva'].sum()
pprint(EMP)

KIOSK = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'KIOSK'), 'iva'].sum()
pprint(KIOSK)
KIOSKP = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'KIOSK'), 'iva'].sum()
pprint(KIOSKP)

dff = pd.DataFrame({'CATEGORY' : ['CIVIL WORK', 'DESIGN', 'IT', 'EM'],
                    'CONSUNTIVO' : [CIVIL, DESIGN, IT, EM],
                    'PREVENTIVO' : [CIVILP, DESIGNP, ITP, EMP],
                    })
pprint(dff)

# ---- ORA PROVO A DIVIDERE PER SEDE SEMPRE TOTALE PREVENTIVO VS BUDGET -----

# -- MONZA CORTELONGA
# --- CIVIL WORKS
MNZWORK = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'LAVORI') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZWORK)
MNZWORKPREVENTIVO = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'LAVORI') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZWORKPREVENTIVO)

# ---- EM --------
MNZEM = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'EM') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZEM)
MNZEMPREVENTIVO = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'EM') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZEMPREVENTIVO)

# ---- IT --------
MNZIT = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'IT') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZIT)
MNZITPREVENTIVO = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'IT') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZITPREVENTIVO)

# --- DESIGN ---
MNZDS = df.loc[(df['tipologia'] == 'Consuntivo') & (df['area'] == 'DESIGN') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZDS)
MNZDSPREVENTIVO = df.loc[(df['tipologia'] == 'Preventivo') & (df['area'] == 'DESIGN') & (df['sede'] == 'MNZ_CORT'), 'iva'].sum()
pprint(MNZDSPREVENTIVO)

# --- KIOSK ----


dmnz = pd.DataFrame({'CATEGORY' : ['CIVIL WORK', 'DESIGN', 'IT', 'EM'],
                    'CONSUNTIVO' : [MNZWORK, MNZDS, MNZIT, MNZEM],
                    'PREVENTIVO' : [MNZWORKPREVENTIVO, MNZDSPREVENTIVO, MNZITPREVENTIVO, MNZEMPREVENTIVO],
                    })
pprint(dmnz)

#pandas.pivot_table(dff, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All', observed=False, sort=True)



pivot = pd.pivot_table(df, values='iva', index=['sede', 'area'],
                    columns=['tipologia', ], aggfunc=np.sum, fill_value=0)





app = Dash(__name__)
server = app.server

app.layout = html.Div(
    dash_pivottable.PivotTable(
        data=data,
        cols=["tipologia"],
        rows=['sede', 'area'],
        vals=["iva"]
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)