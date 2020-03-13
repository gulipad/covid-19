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
	_Over the past few days, Coronavirus has taken the world by storm. As governments rush to take action to minimize the spread of the disease, we – as citizens – also have to stop and think about the individual contributions we can have to #flattenthecurve.
	We'll be looking at how staying at home and washing our hands frequently can help us beat the disease – using math!_🤓 
	## Let's get started
	The [Basic Reproduction Number](https://en.wikipedia.org/wiki/Basic_reproduction_number),$\ R_0$ of an infection is how many people of a population a typical case might infect. So, an$\ R_0 = 2$ means that a typical case infects 2 more people.
	By **moving the slider below**, you can play around with the$\ R_0$ of COVID-19 and see how changing it would affect the evolution of the disease! You'll find the full explanation below the chart.
	'''
)

######################## Current Scenario ########################
# Total population, N.
N = 6662000
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 =  2, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact and recovery times
R0 = 6.49
Tr = 14
Tc = Tr/R0

R0Int = st.slider('Average number of people infected by each sick person', 1.85, 6.49, 4.00, 0.05)
betaInt = R0Int/Tr
# Contact reasoning rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 1/Tc, 1./Tr
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
	name="Scenario with no safety measures",
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
	'> ### An$\ R_0$ of', R0Int, 'renders', deltaInfections, 'less infections and the peak is delayed by ', deltaDays, 'days with respect to the scenario with no safety measures.'
)
st.write(
	'''
	### :mag_right: Conclusions
	$\ R_0$ is a good predictor of how an infection might evolve. This is the only parameter we – as a society – can change in this mathematical model. We *need* to push this value lower. Why?
	The chart above gives us some clues!
	* The **lower** this value, the **lower** the **peak number** of infected individuals.
	* The **lower** this value, the **later** the peak of infected individuals. 
	
	In other words, a lower$\ R_0$ gives us **less total impact** and **more time** to prepare and care for the infected. If we can push$\ R_0$ below **1**, we're in luck! If **each sick person** infects on average **less than one** person, the disease **dies out**.  So, how do we do this?
	* **Social Distancing :house_with_garden::** We try to stay at home as much as possible. If we all do this, we increase the time between contacts with potential sources of virus. Therefore the chances of infecting people or becoming infected ourselves diminishes and$\ R_0$ decreases!
	* **Hygiene :sweat_drops::clap:: **We keep an eye on our hygiene (i.e. properly wash our hands), avoid touching our face, and try to keep at least 1.5 meters of distance with other people. That way if contacts with a source of virus do ocurr, the probability of contagion is as low as possible, and$\ R_0$ again decreases!

	**Play around with the slider above to lower$\ R_0$*** and see this concept in action!

	**Note:$\ R_0 = 6.49$ is the upper limit seen in some studies. For reference the average value seen across several studies is closer to 2.2.*
	'''
)
st.write(
	'> ### :warning: The sooner you start taking measures, the better! Start today!'
)
st.write(
	'''
	### :thinking_face: So, what's going on?
	This [SIR epidemic model] (https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model_without_vital_dynamics) on which I have based this experiment is governed by 2 parameters: 
	* **The Recovery rate, $\gamma$: ** This is the inverse of the time an infected individual is contagious. For this exercise, I've used 14 days, which is the recommended quarantine period.
	* **The Contact rate, 𝛽:** This is the **key** parameter in this exercise. It represents the typical time between contacts. It's actually the inverse of that, so a *𝛽 = 0.5* means 2 days between contacts. Since we can't really affect $\gamma$, this is the parameter we are actually modifying with our safety measures.

	They happen to be the parameters that make up$\ R_0$:
	'''
)
st.latex(r'''
	R_0 = \frac{\beta}{\gamma},
''')
st.write (
	'''
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
	'''This exercise is modelled after the **Community of Madrid** case. So, I have used a population$\ N = 6.66M$ people, and initial conditions$\ I_{init} = 2$ infected and $\ R_{init} = 0$ recovered.
	Then, I used [historical data](https://www.epdata.es/casos-coronavirus-comunidad-madrid/090fa67e-2256-43bd-a7b8-fdfc443da658) of the evolution of the virus to fit a$\ R_0$ for the *Scenario with no safety measures* of '''
	, 6.49, 'which seemed to adjust quite well to the growth numbers of the first 15 days in Madrid, and happens to coincide with the upper limits of [some studies](https://www.medicalnewstoday.com/articles/coronavirus-may-spread-faster-than-who-estimate#Higher-estimates-than-WHO-predict)'
)
st.write(
	'''>:warning: *Note: This exercise was performed on **12/03/2020**.
	By the time you read this, it is likely the fit no longer applies. Also, I'm not an epidemologist, so take it all with a grain of salt and don't forget to follow your local government health and safety regulations! [Here](https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/) is the code this experiment is inspired by.*'''
)
st.write(
'''
------
Made with :heart: in Madrid by [Gulipad](https://www.linkedin.com/in/imorenopubul/)
'''
)






