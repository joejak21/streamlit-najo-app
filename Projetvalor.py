
import streamlit as st
import pandas as pd 
import investpy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
from math import(pow)



def RSI (data) :
  c = 0
  prices = data['Close']
  while c < len(prices) :
        
    i = 0
    upPrices=[]
    downPrices=[]
    #  Loop to hold up and down price movements
    while i < len(prices):
        if i == 0:
            upPrices.append(0)
            downPrices.append(0)
        else:
            if (prices[i]-prices[i-1])>0:
                upPrices.append(prices[i]-prices[i-1])
                downPrices.append(0)
            else:
                downPrices.append(prices[i]-prices[i-1])
                upPrices.append(0)
        i += 1
    x = 0
    avg_gain = []
    avg_loss = []
    #  Loop to calculate the average gain and loss
    while x < len(upPrices):
        if x <15:
            avg_gain.append(0)
            avg_loss.append(0)
        else:
            sumGain = 0
            sumLoss = 0
            y = x-14
            while y<=x:
                sumGain += upPrices[y]
                sumLoss += downPrices[y]
                y += 1
            avg_gain.append(sumGain/14)
            avg_loss.append(abs(sumLoss/14))
        x += 1
    p = 0
    RS = []
    RSI = []
    #  Loop to calculate RSI and RS
    while p < len(prices):
        if p <15:
            RS.append(0)
            RSI.append(0)
        else:
            RSvalue = (avg_gain[p]/avg_loss[p])
            RS.append(RSvalue)
            RSI.append(100 - (100/(1+RSvalue)))
        p+=1
    
    df_dict = {
        'Date'   : data.index,
        'Prices' : prices,
        'upPrices' : upPrices,
        'downPrices' : downPrices,
        'AvgGain' : avg_gain,
        'AvgLoss' : avg_loss,
        'RS' : RS,
        'RSI' : RSI
    }
    return pd.DataFrame(df_dict, columns = ['Date','Prices', 'upPrices', 'downPrices', 'AvgGain','AvgLoss', 'RS', "RSI"])


def MMA (data,nbre_jour) :
  j=nbre_jour
  k=0
  moyenne=[]
  for i in range(0,data.shape[0]-nbre_jour+1): 
    somme=0
    for valeur in data['Close'][k:j]:
      somme+=valeur
    k+=1
    j+=1
    moyenne.append(somme/nbre_jour)
  return pd.DataFrame({'Date':data.index[nbre_jour-1:len(moyenne)+nbre_jour],'MMA':moyenne})

def MMP (data,nbre_jour) :
  j=nbre_jour
  k=0
  moyenne=[]
  #somme des pondérations
  somme_ponderation=0
  for a in range(1,nbre_jour+1):
    somme_ponderation+=a
  for i in range(0,data.shape[0]-nbre_jour+1): 
    somme=0
    #pondération
    p=1
    for valeur in data['Close'][k:j]:
      somme+=p*valeur
      p=p+1
    k+=1
    j+=1
    moyenne.append(somme/somme_ponderation)
  return pd.DataFrame({'Date':data.index[nbre_jour-1:len(moyenne)+nbre_jour],'MMP':moyenne})

def MME (data,nbre_jour,a) :
  from math import(pow)
  j=nbre_jour
  k=0
  moyenne=[]
  #somme des pondérations
  somme_ponderation=0
  for l in range(0,nbre_jour):
    somme_ponderation+=pow(a,l)
  for i in range(0,data.shape[0]-nbre_jour+1): 
    somme=0
    #pondération
    p=nbre_jour-1
    for valeur in data['Close'][k:j]:
      somme+=pow(a,p)*valeur
      p-=1
    k+=1
    j+=1
    moyenne.append(somme/somme_ponderation)
  return pd.DataFrame({'Date':data.index[nbre_jour-1:len(moyenne)+nbre_jour],'MME':moyenne})

def MACD(data,nbr_jour1,nbr_jour2,a1,a2):
  data1=MME(data,nbr_jour1,a1)
  data2=MME(data,nbr_jour2,a2)
  if nbr_jour1<nbr_jour2:
    d1=data1['MME'][nbr_jour2-nbr_jour1:data1.shape[0]]
    d2=data2['MME']
    moyenne=[d1_elt-d2_elt for d1_elt,d2_elt in zip(d1,d2)]
    return pd.DataFrame({'Date':data2['Date'],'MACD':moyenne})
  else:
    d1=data2['MME'][nbr_jour1-nbr_jour2:data2.shape[0]]
    d2=data1['MME']
    moyenne=[d1_elt-d2_elt for d1_elt,d2_elt in zip(d1,d2)]
    return pd.DataFrame({'Date':data1.index,'MACD':moyenne})


st.sidebar.title("Indicateurs")
start = st.sidebar.date_input('Start', value = pd.to_datetime('2021-12-01'))
end = st.sidebar.date_input('End', value = pd.to_datetime('today'))
st.title("Réalisés par ASSOU Joseph et AKIBODE Y. F. Nathalia")
start1 = start.strftime('%d/%m/%Y')
end1 = end.strftime('%d/%m/%Y')


df = investpy.bonds.get_bond_historical_data('Germany 10Y', start1, end1, as_json=False, order='ascending', interval='Daily')    





 
def main():
    page = st.sidebar.selectbox(
        "Select the type of graph",
        [
            "Close",
            "MMA",
            "MMP",
            "MME",
            "MACD",
            "RSI"
        ]
    )

     
    if page == "MMA":
        
        i = int(st.sidebar.number_input("Entrer le nombre de jours",min_value=2) )
        b = MMA(df,i) 
        a =df  
        #st.line_chart(b.MMA)
        
        fig1 = plt.figure() 
        plt.plot(b.Date,b.MMA,label="MMA")
        plt.plot(df.index,df.Close,label="Close")
        plt.legend()
        st.plotly_chart(fig1)
        #
        #plt.plot(a.index,a.Close,label="Cours")
        #st.pyplot()
        #
        #plt.plot(b.Date,b.MMA,label="MMA")
        
        #st.line_chart(b.MMA)
         
    elif page == "MME":
        i = int(st.sidebar.number_input("Entrer le nombre de jours",min_value=1) )
        j = int(st.sidebar.number_input("Entrer le facteur a",min_value = 0.01) )
        d = MME(df,i,j)
        fig2 = plt.figure()
        plt.plot(d.Date,d.MME,label="MME")
        plt.plot(df.index,df.Close,label="Close")
        plt.legend()
        st.plotly_chart(fig2)
    elif page == "MMP":
        i = int(st.sidebar.number_input("Entrer le nombre de jours",min_value=1) )
        c = MMP(df,i)
        fig3 = plt.figure()
        plt.plot(c.Date,c.MMP,label="MMP")
        plt.plot(df.index,df.Close,label="Close")
        plt.legend()
        st.plotly_chart(fig3)
        #st.line_chart(c.MMP)

    elif page == "Close":
      fig4 = plt.figure()
      plt.plot(df.index,df.Close,label="Close")
      plt.legend()
      st.plotly_chart(fig4)
      
    elif page == "MACD":
      df_essai=MACD(df,12,26,0.15,0.0754)
      df_essai
      nbre_jour=9
      a=0.2
      j=nbre_jour
      k=0
      moyenne=[]
      #somme des pondérations
      somme_ponderation=0
      for l in range(0,nbre_jour):
          somme_ponderation+=pow(a,l)
      for i in range(0,df_essai.shape[0]-nbre_jour+1): 
          somme=0
          #pondération
          p=nbre_jour-1
          for valeur in df_essai['MACD'][k:j]:
            somme+=pow(a,p)*valeur
            p-=1
          k+=1
          j+=1
          moyenne.append(somme/somme_ponderation)
      df_essai_MME=pd.DataFrame({'Date':df_essai.index[nbre_jour-1:len(moyenne)+nbre_jour],'moyenne':moyenne})
      d1=df_essai['MACD'][8:df_essai.shape[0]]
      d2=df_essai_MME['moyenne']
      moyenne=[d1_elt-d2_elt for d1_elt,d2_elt in zip(d1,d2)]
      df_final=pd.DataFrame({'Date':df_essai_MME['Date'],'9EMA':df_essai_MME['moyenne'],'moyenne':moyenne})
      fig5 = make_subplots(rows=1, cols=1)
      
      fig5.append_trace(
    go.Bar(
        x=df_final.Date,
        y=df_final['moyenne'],
        name='histogram',
        marker_color="#FF0000",
    ), row=1, col=1
)
      fig5.append_trace(
    go.Scatter(
        x=df_final.Date,
        y=df_final['9EMA'],
        line=dict(color='#000000', width=2),
        # showlegend=False,
        legendgroup='2',
        name='signal'
    ), row=1, col=1
)
      
     
      st.plotly_chart(fig5)













      
      #plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune="upper"))
      #plt.ylabel('MACD',color="w")
      #st.plotly_chart(fig5)
      #fig5 = plt.figure()
      #plt.plot(df.index,df.Close,label="Close")
      #e = MME(df,9,0.2)
      #f = MACD(df,12,26,0.15,0.0754)
      #plt.plot(e.Date,e.MME,color= "#FF0000")
      #plt.plot(f.Date,f.MACD,color= "#000000")
      #plt.legend()
      #st.plotly_chart(fig5)
    elif page == "RSI":
       a = RSI(df)
       fig6, axs = plt.subplots(2, sharex=True)
       axs[0].plot(df.index,df.Close,label="Close")
       axs[1].plot(a.Date,a.RSI,label="RSI", color="#FF0000")
       axs[1].plot()
       st.plotly_chart(fig6)
       


main()
st.dataframe(df)    



#st.line_chart(d.MME)
#st.line_chart(df.Close)
#st.line_chart(b.MMA)
#st.line_chart(c.MMP)
#st.line_chart(a.RSI)

