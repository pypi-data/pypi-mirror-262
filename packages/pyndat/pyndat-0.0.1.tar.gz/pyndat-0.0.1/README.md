# What is pydat?

 The Python Drought Analysis Tool (pydat) is a python package that automatically derives multi-year streamflow deficit Severity-Duration-Frequency (SDF) curves from streamflow data and empowers users to effortlessly create SDF curves. Also, it synthesizes daily-scale streamflow time series called streamflow analogs representing those SDFs. Alongside its core function, pydat offers several other useful commands, including:

1.	Presenting a comprehensive list of the stations in each state or watershed. 
2.	Displaying the streamflow time series of each USGS station.

 The package has been designed to address the need for streamflow deficit SDFs information and their usage in operational water management amid persistent streamflow drought conditions nationally in the United States (US). The picture below shows a sample of the SDF curves for station 03098600 in the Ohio state. 
 
 ![index](https://user-images.githubusercontent.com/67179927/226765480-5383293e-856c-4ce3-8d6a-495e0418a55c.png)
 
 
 Rainfall and flood frequency analysis methods are well established and widely used in analysis and design studies, including but not limited to stormwater management and design studies and hydraulic structures designs, etc. In contrast, no standard method(s) exist for persistent streamflow drought analysis and guidelines for water planners and managers to use in water supply planning and management studies. Although indices related to streamflow deficits are available in the literature, their limitation in usage in planning and operational way hinders their adaptation and useability among water planning and management agencies and utilities. Pydat has been developed to bridge this research and operations gap.

# Methodology

 The first step in using the pydat package is to obtain the daily streamflow time series for a given region of interest. By utilizing a service called the [National Water Information System (NWIS)](https://waterdata.usgs.gov/nwis/) it obtains the daily mean stream values of U.S. Geological Survey (USGS) stream gauge data as its default source. The user can specify the state of interest by providing different inputs such as its two-letter abbreviation, after which all relevant USGS station information and their IDs will be displayed. The pydat package builds upon the python [USGS dataretrieval package](https://github.com/DOI-USGS/dataretrieval-python/) for data retrieval from the USGS website. Furthermore, it should be noted that pydat can also work with other data sources (such as CSV files) with just a few simple tips about the data table and heading columns, as explained in the upcoming sections. 
 
 Once a station is selected, pydat develops multi-year streamflow deficit SDFs for that station, allowing the user to specify the SDF duration. The SDFs are then displayed in both tabular and visual forms for the selected duration. It is important to note that the durations are calculated based on the moving average, and the deficit severity is calculated as a departure from the long-term average flow for each duration.
 
 The final step in using pydat is calculating the daily streamflow time series for the points of the developed streamflow deficit SDFs. Since each point on the SDFs represents a specific event of a deficit level, the duration of the deficit, and the return period, a corresponding daily streamflow time series exists for that point. By linking the SDFs with daily resolution streamflow time series, the SDFs can be operationalized, providing water planners and managers with information about the duration, deficit level, and return periods of selected daily streamflow time series. This allows them to test their water supply system’s response to a range of plausible persistent streamflow deficit scenarios. Overall, pydat provides a valuable tool for water planning and management agencies and water researchers in the face of persistent streamflow drought conditions. The figure below shows the steps of the pydat package.
 
 <img width="1024" alt="methodology" src="https://user-images.githubusercontent.com/67179927/226766889-523091ce-c749-484f-8987-c7a98560cea3.png">

# Installation

To use the package first it is required to clone the repository and install the required packages. 

The code needed for doing this part in Google Colab is written in the below cells. 

Some basic Git commands are:
```
!git clone https://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@github.com/savalann/pydat.git

%cd pydat/pydat/

!pip3 install -r requirements.txt
```


