#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 12:57:53 2020

@author: deannetaillieu
"""
# Import necessary modules
import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter

# Import anthropometric data from desktop as a pandas DataFrame
raw_data = pd.read_csv("/Users/deannetaillieu/desktop/Anthropometric Data.csv", header=0)

# Create new DataFrame with the columns needed to plot lean mass index and sum of 7 skinfolds 
raw_data_crop = raw_data.iloc[:, [0, 1, 3, 4, 5, 6, 7, 9, 10, 11]]

# Remove athletes with less than 2 measurements from the DataFrame
two_measurements = raw_data_crop.duplicated(subset=['ID'], keep=False) # create boolean array indicating duplicate ID values 
one_measurement = ~two_measurements # invert boolean array to show non duplicates as 'True'
one_measurement_index = [i for i, val in enumerate(one_measurement) if val] # find  index of athletes with 1 measurement
two_measurements_index = [i for i, val in enumerate(two_measurements) if val] # find index of athletes with 2+ measurements

# Create new DataFrame including only athletes with 2+ measurements and reset the index
anthro_data = raw_data_crop.iloc[two_measurements_index, :] 
anthro_data = anthro_data.reset_index() 
anthro_data = anthro_data.drop(columns='index') 
anthro_data['Date'] = pd.to_datetime(anthro_data['Date']) # Convert 'Date' column to datetime format for Bokeh plot

# Calculate lean mass index (weight / (sum of 7 skinfolds **0.14)) and sum of 7 skinfolds (triceps, subscap, biceps, illiac, abdomen, thigh, and calf)
# Equations were adapted from Slater et al., (2006) https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2491976/
anthro_data['Lean Mass Index'] = anthro_data['Weight'] / ((anthro_data['Triceps (mm)'] + anthro_data['SubScap (mm)'] + anthro_data['Biceps (mm)'] + anthro_data['Illiac (mm)'] + anthro_data['Abdomen (mm)'] + anthro_data['Thigh (mm)'] + anthro_data['Calf (mm)']) ** 0.14)
anthro_data['Sum of 7'] = anthro_data['Triceps (mm)'] + anthro_data['SubScap (mm)'] + anthro_data['Biceps (mm)'] + anthro_data['Illiac (mm)'] + anthro_data['Abdomen (mm)'] + anthro_data['Thigh (mm)'] + anthro_data['Calf (mm)']
    
# Plot lean mass index for all athletes
data = ColumnDataSource(data=anthro_data)

p1 = figure(x_axis_type='datetime', 
            x_axis_label='Measurement Date', 
            y_axis_label='Lean Mass Index (mm.kg^−0.14)', 
            tools="", 
            toolbar_location=None)
p1.circle(x='Date', 
          y='Lean Mass Index', 
          color='salmon', 
          alpha=0.7, 
          size=10, 
          source=data)
p1.title.text = 'Lean Mass Index of All Athletes'
p1.title.align = "center"
p1.title.text_color = "salmon"
p1.title.text_font_size = "20px"
p1.title.background_fill_color = "white"
p1.title.text_font='helvetica'
p1.title.text_alpha=0.8
p1.xaxis.formatter = DatetimeTickFormatter(months="%B %Y", years="%B %Y")
p1.xaxis.major_label_orientation = 3/4

# Add HoverTool showing exact lean mass index and date values
hover = HoverTool(tooltips=[('Athlete ID', '@ID'), 
                            ('Lean Mass Index', '@{Lean Mass Index}'), 
                            ('Date', '@Date{%F}')], 
                  formatters={'@Date':'datetime'})
p1.add_tools(hover)

# Plot sum of 7 skinfolds for all athletes
p2 = figure(x_axis_type='datetime',
            x_axis_label='Measurement Date',
            y_axis_label='Sum of 7 Skinfolds (mm)',
            tools="", 
            toolbar_location=None)
p2.circle(x='Date', 
          y='Sum of 7', 
          color='cadetblue', 
          alpha=0.7, 
          size=10, 
          source=data)
p2.title.text = 'Sum of 7 Skinfolds of All Athletes'
p2.title.align = "center"
p2.title.text_color = "cadetblue"
p2.title.text_font_size = "20px"
p2.title.background_fill_color = "white"
p2.title.text_font='helvetica'
p2.title.text_alpha=0.8
p2.xaxis.formatter = DatetimeTickFormatter(months="%B %Y", years="%B %Y")
p2.xaxis.major_label_orientation = 3/4

# Add HoverTool showing exact sum of 7 and date values
hover = HoverTool(tooltips=[('Athlete ID', '@ID'), 
                            ('Sum of 7 Skinfolds', '@{Sum of 7}'), 
                            ('Date', '@Date{%F}')], 
                  formatters={'@Date':'datetime'})
p2.add_tools(hover)

# Alter layout so both graphs appear side by side in a row
layout = row(p1, p2)
show(layout)

# Define function 'athlete' that graphs lean mass index and sum of 7 skinfolds for individual athletes using Bokeh
def athlete(ID):
    
    """When athlete ID is inputted into the function, produce two interactive graphs: lean mass index and sum of 7 skinfolds."""
    
    # Gather rows where ID column matches the ID inputted along with all columns associated with those rows and sort by date
    athlete_rows = anthro_data.loc[anthro_data['ID'] == ID, :]
    athlete_rows = athlete_rows.sort_values('Date')
    
    # Create DataFrame and Column Data Source with columns 'ID', 'Date', 'Lean Mass Index' and 'Sum of 7'
    athlete_data = athlete_rows[['ID','Date', 'Lean Mass Index', 'Sum of 7']]
    data = ColumnDataSource(data=athlete_data)
    
    # Plot change in lean mass index over time 
    p3 = figure(x_axis_type='datetime', 
                x_axis_label='Measurement Date', 
                y_axis_label='Lean Mass Index (mm.kg^−0.14)', 
                tools="", 
                toolbar_location=None)
    p3.line(x='Date', 
            y='Lean Mass Index', 
            line_width=2, 
            color='lightslategray', 
            alpha=0.5, 
            line_dash=[5,5], 
            source=data)
    p3.circle(x='Date', 
              y='Lean Mass Index', 
              size=15, 
              color='salmon', 
              alpha=0.8, 
              source=data)
    p3.title.text = f'Lean Mass Index of Athlete {ID}'
    p3.title.align = "center"
    p3.title.text_color = "salmon"
    p3.title.text_font_size = "20px"
    p3.title.background_fill_color = "white"
    p3.title.text_font='helvetica'
    p3.title.text_alpha=0.8
    p3.xaxis.formatter = DatetimeTickFormatter(months="%B %Y", years="%B %Y")
    p3.xaxis.major_label_orientation = 3/4
    
    # Add HoverTool showing the exact lean mass index and measurement date values
    hover = HoverTool(tooltips=[('Lean Mass Index', '@{Lean Mass Index}'), 
                                ('Date', '@Date{%F}')], 
                      formatters={'@Date':'datetime'}, 
                      mode='vline')
    p3.add_tools(hover)
 
    # Plot change in sum of 7 skinfolds over time
    p4 = figure(x_axis_type='datetime', 
                x_axis_label='Measurement Date', 
                y_axis_label='Sum of 7 Skinfolds (mm)', 
                tools="", 
                toolbar_location=None)
    p4.line(x='Date', 
            y='Sum of 7', 
            line_width=2, 
            color='lightslategray', 
            alpha=0.5, 
            line_dash=[5,5], 
            source=data)
    p4.circle(x='Date', 
              y='Sum of 7', 
              size=15, 
              color='cadetblue', 
              alpha=0.8, 
              source=data)
    p4.title.text = f'Sum of 7 Skinfolds of Athlete {ID}'
    p4.title.align = "center"
    p4.title.text_color = "cadetblue"
    p4.title.text_font_size = "20px"
    p4.title.background_fill_color = "white"
    p4.title.text_font='helvetica'
    p4.title.text_alpha=0.8
    p4.xaxis.formatter = DatetimeTickFormatter(months="%B %Y", years="%B %Y")
    p4.xaxis.major_label_orientation = 3/4

    # Add HoverTool showing the exact sum of 7 and date values
    hover = HoverTool(tooltips=[('Sum of 7 Skinfolds', '@{Sum of 7}'), 
                                ('Date', '@Date{%F}')], 
                      formatters={'@Date':'datetime'}, 
                      mode='vline')
    p4.add_tools(hover)
    
    # Alter layout so both graphs appear side by side in a row
    layout2 = row(p3, p4)
    show(layout2)
    
# # Use for loop to generate graphs of all athletes using the athlete function
for i in range(len(anthro_data['ID'].unique())):
    athlete(anthro_data['ID'].unique()[i])

# Export the DataFrame to an Excel file  
# Create Pandas Excel writer using XlsxWriter as the engine 
writer = pd.ExcelWriter("anthropometric_dataframe.xlsx",  
                        engine='xlsxwriter',
                        datetime_format='mmm d yyyy') # set the default datetime format 

# Convert the DataFrame to an XlsxWriter Excel object
anthro_data.to_excel(writer, sheet_name='Sheet1', index=False) 
workbook  = writer.book # get the xlsxwriter workbook and worksheet objects in order to set the column widths to make the dates clearer
worksheet = writer.sheets['Sheet1']
worksheet.set_column('A:A', 15)
writer.save() # close the Pandas Excel writer and output the Excel file.