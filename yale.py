import pandas as pd
# from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.subheader ('Takahashi-Alexander Private Fund Cashflow Model (Yale Model) Demo   :rocket:')
st.caption ('*This is a demo of the 2002 private investment cash flow model developed in Yale.*')

a, b, c = st.columns ([1,1,1])

with a:
    terms =st.number_input ('The life of the fund in years:', value =10)
    bow =st.number_input ('Distribution Bow:', value = 2.0)
    growth_rate = st.number_input ('Growth rate of the portfoli company:', value =0.20) +1
    commitment = st.number_input ('Commitment Size $:', value = 1000)
with b:
    crate1 =st.number_input ('Contribution rate for year 1:', value = 0.25)
    crate2 =st.number_input ('Contribution rate for year 2:', value = 0.25)
    crate3 =st.number_input ('Contribution rate for year 3:', value = 0.25)
    crate4 =st.number_input ('Contribution rate for year 4 and after:', value = 0.25)


crate =[crate1, crate2, crate3, crate4]
# print (crate)
nav = []
contribution =[]
distribution =[]

for i in range (terms):  # loop through every year
    crate_temp = 0
    cash =0 
    unfund = commitment - sum(contribution)
    
    if i>=len(crate):
        crate_temp =crate[-1]  # use the last specified contribution rate 
    else:
        crate_temp =crate[i]

    call = unfund * crate_temp

    if i==0:
        nav.append (call)
    else:
        cash = nav[i-1]*(i/terms)**bow
        nav.append (nav[i-1]*growth_rate + call -cash)

    contribution.append (call)
    distribution.append (cash)

MOIC = (sum(distribution)+nav[-1]) / sum(contribution)

with c:
    st.write ('\n\nSum of cap calls:', round(sum(contribution)))
    st.write ('Sum of cash distribution:', round(sum(distribution)))
    st.write ('MOIC: ', round(MOIC,2), '\n\n')

# print (contribution)
# print (distribution)
# print (nav[-1], '\n')

x_indexes = np.arange (terms)
width=0.25
fig, ax = plt.subplots()

plt.bar (x_indexes-width, contribution, width=width, label='Cap Call')
plt.bar (x_indexes, nav, width=width, label='Nav')
plt.bar (x_indexes+width, distribution, width=width, label='Cash Dis.')
# plt.plot (x_indexes, cashflow_data['netCF'], color ='green', marker='o', linestyle='--', label='netCF')

ax.set_title('Cash Flow')
ax.set_xlabel('Year')
ax.set_ylabel('Dollars')
ax.legend()

plt.xticks (ticks =x_indexes, labels= x_indexes+1, rotation =0)
plt.tight_layout()

st.pyplot(fig)

df =pd.DataFrame({
    'Contribution': contribution,
    'Distribution': distribution,
    'Net Asset Value': nav
    })

st.write(df)




