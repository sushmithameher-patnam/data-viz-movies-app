from flask import Flask, render_template
from pandas import pandas as pd
import altair as alt


app = Flask(__name__)

def startupDataFrame():
    csv_url='https://gist.githubusercontent.com/sushmithameher-patnam/f0b351cb272aa9714a5b729851b8a637/raw/6bd1e133ba2770677f5fa5ef5b1a226370805add/MoviesOnStreamingPlatforms_cleanedfinal.csv'
    data=pd.read_csv(csv_url)
    data=data.dropna()
    dict_18_plus={
    "Netflix":0,
    "Hulu":0,
    "Disney+":0,
    "Prime Video":0
    }
    dict_16={
    "Netflix":0,
    "Hulu":0,
    "Disney+":0,
    "Prime Video":0
    }
    dict_13={
    "Netflix":0,
    "Hulu":0,
    "Disney+":0,
    "Prime Video":0   
    }
    dict_7={
    "Netflix":0,
    "Hulu":0,
    "Disney+":0,
    "Prime Video":0   
    }
    dict_all={
    "Netflix":0,
    "Hulu":0,
    "Disney+":0,
    "Prime Video":0   
    }

    for i in data.index:
        if data["Age"][i]=='18+':
            dict_18_plus[data["OTT_Name"][i]]+=1
        elif data["Age"][i]=='16+':
            dict_16[data["OTT_Name"][i]]+=1
        elif data["Age"][i]=='13+':
            dict_13[data["OTT_Name"][i]]+=1
        elif data["Age"][i]=='7+':
            dict_7[data["OTT_Name"][i]]+=1
        elif data["Age"][i]=='all':
            dict_all[data["OTT_Name"][i]]+=1
    
    List_of_all_age_groups=[]
    List_of_all_age_groups.append(dict_18_plus)
    List_of_all_age_groups.append(dict_16)
    List_of_all_age_groups.append(dict_13)
    List_of_all_age_groups.append(dict_7)
    List_of_all_age_groups.append(dict_all)        

    df=pd.DataFrame(data=List_of_all_age_groups)

    df["Age Group"]=["18+","16+","13+","7+","all"]
    return df

def firstDataCleaner():
    
    df = startupDataFrame()
    df1=df.drop("Age Group",axis=1)
    df1=df1.sum()
    df1= df1.reset_index().rename(columns={'index': 'Platform', 0: "Count"})

    chart_platform = alt.Chart(df1).mark_bar().encode(
    x=alt.X('Platform', axis=alt.Axis(labelAngle=-45)),
    y='Count',
    color=alt.Color('Platform:N',scale=alt.Scale(scheme='category20')),
    tooltip=['Count']
    )
    print(chart_platform.to_json())
    return chart_platform.to_json()
            
def secondDataChart():
    df = startupDataFrame()
    selection = alt.selection_multi(fields=['Age Group'], bind='legend')
    Pie_chart=alt.Chart(df).mark_arc().encode(
    theta="Netflix",
    color=alt.Color('Age Group:N',scale=alt.Scale(scheme='redpurple')),
    tooltip="Netflix",
    opacity=alt.condition(selection, alt.value(1), alt.value(0))   
    ).add_selection(
    selection
    ).interactive()

    return Pie_chart.to_json()

def secondSubDataChart1():
    df = startupDataFrame()
    selection = alt.selection_multi(fields=['Age Group'], bind='legend')
    Pie_chart_hulu=alt.Chart(df).mark_arc().encode(
    theta="Hulu",
    color=alt.Color('Age Group:N',scale=alt.Scale(scheme='dark2')),
    tooltip="Hulu",
    opacity=alt.condition(selection, alt.value(1), alt.value(0))   
    ).add_selection(
    selection
    ).interactive()
    return Pie_chart_hulu.to_json()

def secondSubDataChart2():
    df = startupDataFrame()
    selection = alt.selection_multi(fields=['Age Group'], bind='legend')
    Pie_chart_disney=alt.Chart(df).mark_arc().encode(
    theta="Disney+",
    color=alt.Color('Age Group:N',scale=alt.Scale(scheme='paired')),
    tooltip="Disney+",
    opacity=alt.condition(selection, alt.value(1), alt.value(0))   
    ).add_selection(
    selection
    ).interactive()
    return Pie_chart_disney.to_json()

def secondSubDataChart3():
    df = startupDataFrame()
    selection = alt.selection_multi(fields=['Age Group'], bind='legend')
    Pie_chart_primevideo=alt.Chart(df).mark_arc().encode(
    theta="Prime Video",
    color=alt.Color('Age Group:N',scale=alt.Scale(scheme='accent')),
    tooltip="Prime Video",
    opacity=alt.condition(selection, alt.value(1), alt.value(0))   
    ).add_selection(
    selection
    ).interactive()
    return Pie_chart_primevideo.to_json()



def getScatterChart():
    csv_url='https://gist.githubusercontent.com/sushmithameher-patnam/f0b351cb272aa9714a5b729851b8a637/raw/6bd1e133ba2770677f5fa5ef5b1a226370805add/MoviesOnStreamingPlatforms_cleanedfinal.csv'
    data=pd.read_csv(csv_url)
    data=data.dropna()
    Ratings_chart=alt.Chart(data).mark_point().encode(
    x='OTT_Name',y='Rotten Tomatoes',tooltip=['Title','Rotten Tomatoes'],
    color=alt.Color('Rotten Tomatoes:N',scale=alt.Scale(scheme='category20b')),
    ).properties(width=500,height=500)
    return Ratings_chart.to_json()

def getStackedBarChart ():
    
    data11=pd.read_csv(r'/Users/mehersushu/Downloads/MoviesOnStreamingPlatforms-filtered.csv')
    grouped = data11.groupby(['Genre', 'OTT_Name']).size().reset_index(name='count')
    StackedBarChart= alt.Chart(grouped).mark_bar().encode(
    x='OTT_Name',
    y= 'count',
    color= 'Genre:N',
    tooltip=['Genre','OTT_Name','count']
    ).properties(
    width=500,
    height=500,
    title='All Movies by Genre and OTT Name'
    ).configure_axis(
    labelAngle=0
    )
    return StackedBarChart.to_json()


@app.route('/')
def visualizations():
    return render_template("index.html" , 
                           chartData = firstDataCleaner(), 
                            )
@app.route('/layout1')
def layout1():
    return render_template("layout1.html",
                           chartData2=secondDataChart(),
                           chartData3=secondSubDataChart1(),
                           chartData4=secondSubDataChart2(),
                           chartData5=secondSubDataChart3())
@app.route('/layout2')
def layout2():
    return render_template("layout2.html",
                            chartData6 = getScatterChart())
@app.route('/layout3')
def layout3():
    return render_template("layout3.html",
                           chartData7=getStackedBarChart())