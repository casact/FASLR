import chainladder as cl
import pandas as pd

df_uspp = pd.read_csv("faslr/samples/friedland_uspp_auto_steady_state.csv")


tri_uspp = cl.Triangle(
    data=df_uspp,
    origin="Accident Year",
    development="Calendar Year",
    columns=["Paid Claims", "Reported Claims"],
    cumulative=True
)

tri_uspp["Paid Claims"]

tri_uspp['Reported Claims']

tri_uspp["Reported Claims"].link_ratio