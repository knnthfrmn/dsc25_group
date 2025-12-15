# App to reach final combined_df from notebook (copypasting all preprocessing cells)

import pandas as pd

def load_and_prepare_data():
    unemployment_data = pd.read_csv('data/global_unemployment_data.csv')
    happiness_2015 = pd.read_csv('data/happiness data/2015.csv')
    happiness_2016 = pd.read_csv('data/happiness data/2016.csv')
    happiness_2017 = pd.read_csv('data/happiness data/2017.csv')
    happiness_2018 = pd.read_csv('data/happiness data/2018.csv')
    happiness_2019 = pd.read_csv('data/happiness data/2019.csv')
    happiness_2015['Year'] = 2015
    happiness_2016['Year'] = 2016
    happiness_2017['Year'] = 2017
    happiness_2018['Year'] = 2018
    happiness_2019['Year'] = 2019
    happiness_2015 = happiness_2015.rename(columns={'Economy (GDP per Capita)': 'GDP per cap', 
                                                    'Health (Life Expectancy)': 'Life Expectancy', 
                                                    'Trust (Government Corruption)': 'Corruption'})
    happiness_2015 = happiness_2015.drop(columns={'Region', 'Standard Error', 'Dystopia Residual'})
    happiness_2016 = happiness_2016.rename(columns={'Economy (GDP per Capita)': 'GDP per cap', 
                                                    'Health (Life Expectancy)': 'Life Expectancy', 
                                                    'Trust (Government Corruption)': 'Corruption'})
    happiness_2016 = happiness_2016.drop(columns={'Region', 'Lower Confidence Interval', 'Upper Confidence Interval', 'Dystopia Residual'})
    happiness_2017 = happiness_2017.rename(columns={'Happiness.Rank': 'Happiness Rank', 
                                                    'Happiness.Score': 'Happiness Score', 
                                                    'Economy..GDP.per.Capita.': 'GDP per cap',
                                                    'Health..Life.Expectancy.': 'Life Expectancy',
                                                    'Trust..Government.Corruption.': 'Corruption'})
    happiness_2017 = happiness_2017.drop(columns={'Whisker.high', 'Whisker.low', 'Dystopia.Residual'})
    happiness_2018 = happiness_2018.rename(columns={'GDP per capita': 'GDP per cap',
                                                    'Country or region': 'Country',
                                                    'Score': 'Happiness Score',
                                                    'Overall rank': 'Happiness Rank',
                                                    'Social support': 'Family',
                                                    'Healthy life expectancy': 'Life Expectancy',
                                                    'Perceptions of corruption': 'Corruption',
                                                    'Freedom to make life choices': 'Freedom'})
    happiness_2019 = happiness_2019.rename(columns={'GDP per capita': 'GDP per cap',
                                                    'Country or region': 'Country',
                                                    'Score': 'Happiness Score',
                                                    'Overall rank': 'Happiness Rank',
                                                    'Social support': 'Family',
                                                    'Healthy life expectancy': 'Life Expectancy',
                                                    'Perceptions of corruption': 'Corruption',
                                                    'Freedom to make life choices': 'Freedom'})
    happiness_data = pd.concat([happiness_2015, happiness_2016, happiness_2017, happiness_2018, happiness_2019])
    happiness_data = happiness_data.reset_index()
    happiness_data = happiness_data.drop(columns={'index'})
    drop = ['2014','2020','2021','2022','2023','2024']
    unemployment_data = unemployment_data.drop(columns = drop)
    unemployment_data['Country'] = unemployment_data['country_name']
    happiness_data['Country'] = happiness_data['Country'].replace({'Congo (Kinshasa)':'Congo, Democratic Republic of the'})
    happiness_data['Country'] = happiness_data['Country'].replace({'Congo (Brazzaville)':'Congo'})
    happiness_data['Country'] = happiness_data['Country'].replace({'Iran':'Iran, Islamic Republic of'})
    unemployment_data['Country'] = unemployment_data['Country'].replace({'Viet Nam':'Vietnam'})
    unemployment_data['Country'] = unemployment_data['Country'].replace({'Czechia':'Czech Republic'})
    happiness_data['Country'] = happiness_data['Country'].replace({'Hong Kong S.A.R., China':'Hong Kong'})
    happiness_data['Country'] = happiness_data['Country'].replace({'Taiwan Provice of China':'Taiwan'})
    unemployment_data['Country'] = unemployment_data['Country'].replace({'Taiwan, China':'Taiwan'})
    year_cols = ['2015', '2016', '2017', '2018', '2019']
    long_unemp = unemployment_data.melt(
        id_vars=['country_name', 'sex', 'age_group', 'age_categories', 'Country'],
        value_vars=year_cols,
        var_name='year',
        value_name='unemployment_rate'
    )
    long_unemp['year'] = long_unemp['year'].astype(int)
    long_unemp.drop(columns=['country_name', 'sex', 'age_categories'])
    avg_country_year = (long_unemp.groupby(['Country', 'year'])['unemployment_rate'].mean().reset_index())
    avg_country_year = avg_country_year.rename(columns={'year': 'Year', 'unemployment_rate' : 'Unemployment'})
    avg_country_year['Country Year'] = avg_country_year['Country'].astype(str) + '_' + avg_country_year['Year'].astype(str)
    happiness_data['Country Year'] = happiness_data['Country'].astype(str) + '_' + happiness_data['Year'].astype(str)
    combined_df = pd.merge(happiness_data, avg_country_year, on=['Country Year'])
    drop_2 = ['Country_x','Year_x']
    combined_df = combined_df.drop(columns = drop_2)
    combined_df = combined_df.rename(columns={'Country_y':'Country','Year_y':'Year'})
    
    return combined_df