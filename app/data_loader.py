import pandas as pd
import aiohttp
import asyncio
import io
import numpy as np

class DataLoader:
    def __init__(self):
        self.dataframe = pd.DataFrame()
        # Dictionary to map countries to continents (simplified version)
        self.country_to_continent = {
            # This is a simplified mapping - in production, use a comprehensive dataset
            'Colombia': 'South America',
            'Brazil': 'South America',
            'Peru': 'South America',
            'Ecuador': 'South America',
            'Venezuela': 'South America',
            'Argentina': 'South America',
            'Chile': 'South America',
            'United States': 'North America',
            'Canada': 'North America',
            'Mexico': 'North America',
            'Spain': 'Europe',
            'France': 'Europe',
            'Germany': 'Europe',
            'United Kingdom': 'Europe',
            'Italy': 'Europe',
            'Nigeria': 'Africa',
            'South Africa': 'Africa',
            'Egypt': 'Africa',
            'Kenya': 'Africa',
            'China': 'Asia',
            'India': 'Asia',
            'Japan': 'Asia',
            'Australia': 'Oceania',
            'New Zealand': 'Oceania'
        }

    async def fetch_csv(self):
        CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(CSV_URL) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        self.dataframe = pd.read_csv(io.BytesIO(content))
                        print(f"Data loaded successfully, DataFrame size: {len(self.dataframe)}")
                        
                        # Ensure appropriate data types
                        if 'Year' in self.dataframe.columns:
                            self.dataframe['Year'] = pd.to_numeric(self.dataframe['Year'], errors='coerce')
                        
                        # Handle potential column names
                        birth_rate_col = None
                        country_col = None
                        
                        for col in self.dataframe.columns:
                            if col in ['Country', 'Entity', 'Nation', 'Country Name']:
                                country_col = col
                            elif 'birth' in col.lower() and 'rate' in col.lower():
                                birth_rate_col = col
                                self.dataframe[col] = pd.to_numeric(self.dataframe[col], errors='coerce')
                        
                        # Add continent column based on country
                        if country_col:
                            self.dataframe['Continent'] = self.dataframe[country_col].apply(
                                lambda x: self.country_to_continent.get(x, 'Unknown')
                            )
                        
                        return True
                    else:
                        print(f"Error downloading data: {resp.status}")
                        return False
        except Exception as e:
            print(f"Exception during data fetch: {e}")
            return False

    async def get_data_html(self):
        if self.dataframe.empty:
            return "<p>No data available.</p>", 0
        else:
            df = self.dataframe.head(100)  # Show only the first 100 records
            table_html = df.to_html(classes="table table-striped table-bordered table-hover", 
                                    index=False, 
                                    border=0,
                                    justify="center")
            return table_html, len(self.dataframe)
    
    async def get_birth_rate_by_year(self):
        """Returns average birth rate by year across all countries"""
        if self.dataframe.empty:
            return []
        
        # Identifying the birth rate column
        birth_rate_col = None
        for col in self.dataframe.columns:
            if 'birth' in col.lower() and 'rate' in col.lower():
                birth_rate_col = col
                break
        
        if not birth_rate_col:
            return []
            
        yearly_avg = self.dataframe.groupby('Year')[birth_rate_col].mean().reset_index()
        return yearly_avg.to_dict(orient='records')
    
    async def get_countries_list(self):
        """Returns the list of all countries in the dataset"""
        if self.dataframe.empty:
            return []
        
        # Find the column containing country names
        country_col = None
        possible_names = ['Country', 'Entity', 'Nation', 'Country Name']
        for col in possible_names:
            if col in self.dataframe.columns:
                country_col = col
                break
        
        if not country_col:
            return []
            
        countries = self.dataframe[country_col].unique().tolist()
        return sorted(countries)
    
    async def get_top_countries_by_birth_rate(self, year=None, top_n=10, ascending=False):
        """Returns countries with highest/lowest birth rates for a given year or latest available"""
        if self.dataframe.empty:
            return []
        
        # Identify relevant columns
        country_col = None
        birth_rate_col = None
        
        for col in self.dataframe.columns:
            if col in ['Country', 'Entity', 'Nation', 'Country Name']:
                country_col = col
            elif 'birth' in col.lower() and 'rate' in col.lower():
                birth_rate_col = col
        
        if not country_col or not birth_rate_col:
            return []
        
        # Filter by year if specified
        if year:
            df_filtered = self.dataframe[self.dataframe['Year'] == year].copy()
        else:
            # Get the latest year for each country
            latest_year = self.dataframe.groupby(country_col)['Year'].max().reset_index()
            df_filtered = pd.merge(self.dataframe, latest_year, on=[country_col, 'Year'])
        
        # Calculate average birth rate per country
        country_avg = df_filtered.groupby(country_col)[birth_rate_col].mean().reset_index()
        country_avg = country_avg.sort_values(birth_rate_col, ascending=ascending).head(top_n)
        
        return country_avg.to_dict(orient='records')
    
    async def get_country_trend(self, country_name):
        """Returns birth rate trend over years for a specific country"""
        if self.dataframe.empty:
            return []
        
        # Identify relevant columns
        country_col = None
        birth_rate_col = None
        
        for col in self.dataframe.columns:
            if col in ['Country', 'Entity', 'Nation', 'Country Name']:
                country_col = col
            elif 'birth' in col.lower() and 'rate' in col.lower():
                birth_rate_col = col
        
        if not country_col or not birth_rate_col:
            return []
        
        # Filter by country
        country_data = self.dataframe[self.dataframe[country_col] == country_name].copy()
        country_data = country_data.sort_values('Year')
        
        result = country_data[['Year', birth_rate_col]].to_dict(orient='records')
        return result
    
    async def get_comparative_data(self, reference_country='Colombia', comparison_countries=None, latest_only=False):
        """Returns data comparing reference country with others"""
        if self.dataframe.empty:
            return {}
        
        # Identify relevant columns
        country_col = None
        birth_rate_col = None
        
        for col in self.dataframe.columns:
            if col in ['Country', 'Entity', 'Nation', 'Country Name']:
                country_col = col
            elif 'birth' in col.lower() and 'rate' in col.lower():
                birth_rate_col = col
        
        if not country_col or not birth_rate_col:
            return {}
        
        # If no comparison countries provided, use top 5
        if not comparison_countries:
            top_countries = await self.get_top_countries_by_birth_rate(top_n=5)
            comparison_countries = [country[country_col] for country in top_countries 
                                   if country[country_col] != reference_country][:4]  # Limit to 4
        
        # Add reference country to the list
        countries_to_compare = [reference_country] + comparison_countries
        
        # Filter data to include only these countries
        filtered_data = self.dataframe[self.dataframe[country_col].isin(countries_to_compare)].copy()
        
        if latest_only:
            # Get only latest year data
            latest_year = filtered_data.groupby(country_col)['Year'].max().reset_index()
            result_data = pd.merge(filtered_data, latest_year, on=[country_col, 'Year'])
        else:
            result_data = filtered_data
            
        # Ensure we're working with sorted data
        result_data = result_data.sort_values(['Year', country_col])
        
        # Structure data for easy consumption in charts
        comparative_data = {}
        for country in countries_to_compare:
            country_data = result_data[result_data[country_col] == country]
            comparative_data[country] = country_data[['Year', birth_rate_col]].to_dict(orient='records')
        
        return comparative_data
    
    # New methods for the additional API endpoints
    async def get_all_countries_latest_year(self, limit=50):
        """Returns the latest birth rate data for all countries"""
        if self.dataframe.empty:
            return []
        
        # Identify relevant columns
        country_col = None
        birth_rate_col = None
        
        for col in self.dataframe.columns:
            if col in ['Country', 'Entity', 'Nation', 'Country Name']:
                country_col = col
            elif 'birth' in col.lower() and 'rate' in col.lower():
                birth_rate_col = col
        
        if not country_col or not birth_rate_col:
            return []
        
        # Get the latest year for each country
        latest_year = self.dataframe.groupby(country_col)['Year'].max().reset_index()
        latest_data = pd.merge(self.dataframe, latest_year, on=[country_col, 'Year'])
        
        # Sort by birth rate and limit number of countries if needed
        if limit > 0:
            latest_data = latest_data.sort_values(birth_rate_col, ascending=False).head(limit)
        else:
            latest_data = latest_data.sort_values(birth_rate_col, ascending=False)
        
        result = latest_data[[country_col, 'Year', birth_rate_col]].to_dict(orient='records')
        return result
    
    async def get_continent_trend(self, continent_name=None):
        """Returns birth rate trends by continent"""
        if self.dataframe.empty or 'Continent' not in self.dataframe.columns:
            return {}
        
        # Identify birth rate column
        birth_rate_col = None
        for col in self.dataframe.columns:
            if 'birth' in col.lower() and 'rate' in col.lower():
                birth_rate_col = col
                break
        
        if not birth_rate_col:
            return {}
        
        # Filter by continent if specified
        if continent_name and continent_name.lower() != 'all':
            df_filtered = self.dataframe[self.dataframe['Continent'] == continent_name].copy()
        else:
            df_filtered = self.dataframe.copy()
        
        # Calculate average birth rate by continent and year
        continent_trend = df_filtered.groupby(['Continent', 'Year'])[birth_rate_col].mean().reset_index()
        
        # Structure data for chart consumption
        trend_data = {}
        for continent, data in continent_trend.groupby('Continent'):
            trend_data[continent] = data[['Year', birth_rate_col]].to_dict(orient='records')
        
        return trend_data
    
    async def get_continents_list(self):
        """Returns list of continents in the dataset"""
        if self.dataframe.empty or 'Continent' not in self.dataframe.columns:
            return []
        
        continents = self.dataframe['Continent'].unique().tolist()
        return sorted([c for c in continents if c != 'Unknown'])