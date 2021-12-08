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
2. Since the data differ in the absolute number of cases, which depends on many factors, e.g. population density, we propose to test the hypothesis on the influence of temperature on virus development on the basis of the standardized coefficient of virus reproduction R. There are several methods to determine this coefficient, but let us assume a very simplified method, which consists in comparing the number of cases in periods of 1 week.

Meteorological data

Meteorological data on the minimum and maximum temperature for the month (2018 data) are available in the file
https://chmura.put.poznan.pl/s/8GI44MgN9zwRQAX
https://chmura.put.poznan.pl/s/6PUjoY9LOx8VKL8
Determine the estimate of the mean temperature expressed as the average of the extreme temperatures.

Hypothesis testing
Test the following hypotheses for the data set

Ambient temperature significantly affects the rate of virus spread. Assume that we conduct the analysis for the variables, which are discrete ranges of average temperature values per month [<0; 0-10, 10-20, 20-30, 30>]. In turn, the value analyzed is the normalized value of the reproduction coefficient determined separately for each country/region (determine the value by dividing all reproduction coefficients by the maximum value observed for the country). If you get significant differences, conduct a post-hoc analysis.

Investigate whether there are significant differences in COVID-19 mortality between countries in Europe. Perform the analysis in 2 ways:

using the chi2 test of independence, where the data will be the total number of deaths to the total number of infections
using ANOVA, where the variable is country and the observed values are mortality per month.
Try to interpret the differences that may occur.
