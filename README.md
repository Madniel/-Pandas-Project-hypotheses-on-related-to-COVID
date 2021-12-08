# Pandas-Project-hypotheses-on-related-to-COVID

COVID-19 data
Information about covid comes from 3 datasets maintained by CSSE at Johns Hopkins University: the repository. The tables contain the following information:
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

cumulative incidence by country time_series_covid19_confirmed_global.csv
cumulative number of deaths per country time_series_covid19_deaths_global.csv
cumulative number of people who recovered by country time_series_covid19_recovered_global.csv

COVID-19 Metrics
1. Based on the data, determine:
the number of active cases (for each day)
Cumulative mortality for each month, which measures the number of deaths to the number of people who recovered in that month
if a country does not publish results on the number of persons who recovered, assume that the duration of infection is 14 days
if a given country does not publish mortality results, remove it from the list
in further analysis do not include data for less than 100 active cases.
2. Since the data differ in the absolute number of cases, which depends on many factors, e.g. population density, we propose to test the hypothesis on the influence of temperature on virus development on the basis of the standardized coefficient of virus reproduction R. There are several methods to determine this coefficient, but let us assume a very simplified method, which consists in comparing the number of cases in periods of 1 week. As an aid, determine the average number of infections for the last 7 days for day i:
