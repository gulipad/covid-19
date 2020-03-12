import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import plotly.express as px
import plotly.graph_objs as go

st.write(
	'''
	# COVID-19: The mathematical reason to wash your hands :sweat_drops::clap:
	_Over the past few days, Coronavirus has taken the world by storm. As governments rush to take action to minimize the spread of the diseas, I've built this tool to illustrate why these measures – and other measures we can push on an individual basis – are so important.
	We'll be looking at how staying at home and washing our hands frequently can help us beat the disease – using math!_🤓 
	## The SIR Method
	By **moving the slider below**, you can play around with the *Contact rate*, 𝛽 of the virus so see how it would affect the evolution of the disease! You'll find the full explanation below the chart.
	'''
)
betaInt = st.slider('Contact rate, 𝛽', 0.2, 0.4, 0.4, 0.05)

######################## Current Scenario ########################
# Total population, N.
N = 6662000
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 =  1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact reasoningte, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 0.55, 1./14 
# A grid of time points (in days)
t = np.linspace(0, 365, 365)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt
# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

#################### Interactive Scenario ######################
# The SIR model differential equations.
def deriv(yInt, t, N, betaInt, gamma):
    SInt, IInt, RInt = yInt
    dSIntdt = -betaInt * SInt * IInt / N
    dIIntdt = betaInt * SInt * IInt / N - gamma * IInt
    dRIntdt = gamma * IInt
    return dSIntdt, dIIntdt, dRIntdt
# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
retInt = odeint(deriv, y0, t, args=(N, betaInt, gamma))
SInt, IInt, RInt = retInt.T
########################## Charting ##########################
datelist = pd.date_range(start='25/2/2020', periods=220).tolist()
fig = go.Figure()
intTrace = go.Scatter(
	x=datelist,
	y=IInt,
	name="Your Scenario",
	line=dict(color='MediumSeaGreen'),
	fill='tozeroy',
	hovertemplate =
    '<br><b>Date</b>: %{x}<br>' +
    '<b>Infected</b>: %{y:.2s} people'
)
currentTrace = go.Scatter(
	x=datelist, 
	y=I,
	name="Scenario with no safety measures (𝛽 = 0.5)",
	line=dict(color='Red'),
	fill='tozeroy',
	hovertemplate =
    '<br><b>Date</b>: %{x}<br>' +
    '<b>Infected</b>: %{y:.2s} people'
)
fig.update_layout(
    title="Infection Curves",
    xaxis_title="Time (days)",
    yaxis_title="Nº of Infected People",
)
fig.update_layout(
    legend=dict(
        x=0,
        y=-0.2,
        orientation="h"
    )
)
fig.update_layout(hovermode='x')

fig.add_trace(currentTrace)
fig.add_trace(intTrace)
chart = st.plotly_chart(fig)

########################################
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
deltaInfections = human_format(np.amax(I) - np.amax(IInt))
deltaDays = np.argmax(IInt) - np.argmax(I)
st.write(
	'> ### A 𝛽 of', betaInt, 'renders', deltaInfections, 'less infections and the peak is delayed by ', deltaDays, 'days with respect to the scenario with no safety measures.'
)
st.write(
	'''
	### :mag_right: Conclusions
	The parameter 𝛽 represents how often contacts with infected population end in infection. This is the only parameter we – as a society – can change in this mathematical model. We *need* to push this value lower. Why?
	The chart above gives us some clues!
	* The **lower** this value, the **lower** the **peak number** of infected individuals.
	* The **lower** this value, the **later** the peak of infected individuals. 
	
	In other words, a lower 𝛽 gives us **less total impact** and **more time** to prepare and care for the infected. So, how do we do this?
	* :house_with_garden: We try to stay at home as much as possible. If we all do this, we increase the time between contacts.
	* :sweat_drops::clap: We keep an eye on our hygiene (a.k.a. properly wash our hands). That way if contacts do ocurr, the probability of contagion is as low as possible.

	**Play around with the slider above to lower 𝛽** and see this concept in action!
	'''
)
st.write(
	'''
	### :thinking_face: So, what's going on?
	With the [SIR epidemic model] (https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model_without_vital_dynamics) is governed by 2 parameters: 
	* **The Contact rate, 𝛽:** This is the **key** parameter in this exercise. It represents the typical time between contacts. It's actually the inverse of that, so a *𝛽 = 0.5* means 2 days between contacts.
	* **The Recovery rate, $\gamma$: ** This is the inverse of the time an infected individual is contagious. For this exercise, I've used 14 days, which is the recommended quarantine period.

	The SIR model describes the evolution of COVID-19 as a set of ordinary differential equations:
	'''
)
st.latex(r'''
	\frac{dS}{dt} = - \frac{\beta I S}{N},
''')
st.latex(r'''
	\frac{dI}{dt} = \frac{\beta I S}{N} - \gamma I,
''')
st.latex(r'''
	\frac{dR}{dt} = \gamma I
''')
st.write(
	'Where$\ S$ is the stock of susceptible population,$\ I$ is the stock of infected, and$\ R$ is the stock of recovered population.'
)
st.write(
	'''This exercise is modelled after the **Community of Madrid** case. So, I have used a population$\ N = 6.66M$ people, and initial conditions$\ I_0 = 1$ infected and $\ R_0 = 0$ recovered.
	Then, I used [historical data](https://www.epdata.es/casos-coronavirus-comunidad-madrid/090fa67e-2256-43bd-a7b8-fdfc443da658) of the evolution of the virus to fit a 𝛽 for the *Worst Case Scenario* of '''
	, 0.5, 'which seemed to adjust quite well to the growth numbers of the first 15 days in Madrid'
)
st.write(
	'''>:warning: *Note: This exercise was performed on **12/03/2020**.
	By the time you read this, it is likely the fit no longer applies. Also, I'm not an epidemologist, so take it all with a grain of salt and don't forget to follow your local government health and safety regulations!*'''
)






