import pandas as pd
import aiohttp
import asyncio
import io
import numpy as np

class DataLoader:
    def __init__(self):
        self.dataframe = pd.DataFrame()
        # Mapeo de países a continentes (simplificado)
        self.country_to_continent = {
            # América del Norte
            'United States': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
            'Panama': 'North America', 'Costa Rica': 'North America', 'Guatemala': 'North America',
            'Honduras': 'North America', 'El Salvador': 'North America', 'Nicaragua': 'North America',
            'Jamaica': 'North America', 'Haiti': 'North America', 'Dominican Republic': 'North America',
            'Cuba': 'North America', 'Bahamas': 'North America', 'Barbados': 'North America',
            'Trinidad and Tobago': 'North America', 'Belize': 'North America',
            
            # América del Sur
            'Colombia': 'South America', 'Brazil': 'South America', 'Argentina': 'South America',
            'Peru': 'South America', 'Chile': 'South America', 'Ecuador': 'South America',
            'Venezuela': 'South America', 'Bolivia': 'South America', 'Paraguay': 'South America',
            'Uruguay': 'South America', 'Guyana': 'South America', 'Suriname': 'South America',
            
            # Europa
            'United Kingdom': 'Europe', 'France': 'Europe', 'Germany': 'Europe', 'Italy': 'Europe',
            'Spain': 'Europe', 'Portugal': 'Europe', 'Netherlands': 'Europe', 'Belgium': 'Europe',
            'Switzerland': 'Europe', 'Austria': 'Europe', 'Sweden': 'Europe', 'Norway': 'Europe',
            'Denmark': 'Europe', 'Finland': 'Europe', 'Iceland': 'Europe', 'Ireland': 'Europe',
            'Greece': 'Europe', 'Russia': 'Europe', 'Ukraine': 'Europe', 'Poland': 'Europe',
            'Romania': 'Europe', 'Bulgaria': 'Europe', 'Hungary': 'Europe', 'Czech Republic': 'Europe',
            'Slovakia': 'Europe', 'Croatia': 'Europe', 'Serbia': 'Europe', 'Montenegro': 'Europe',
            'Albania': 'Europe', 'North Macedonia': 'Europe', 'Bosnia and Herzegovina': 'Europe',
            'Slovenia': 'Europe', 'Estonia': 'Europe', 'Latvia': 'Europe', 'Lithuania': 'Europe',
            'Belarus': 'Europe', 'Moldova': 'Europe', 'Luxembourg': 'Europe', 'Monaco': 'Europe',
            
            # Asia
            'China': 'Asia', 'India': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia',
            'Indonesia': 'Asia', 'Philippines': 'Asia', 'Vietnam': 'Asia', 'Thailand': 'Asia',
            'Malaysia': 'Asia', 'Singapore': 'Asia', 'Pakistan': 'Asia', 'Bangladesh': 'Asia',
            'Iran': 'Asia', 'Iraq': 'Asia', 'Saudi Arabia': 'Asia', 'Israel': 'Asia',
            'Turkey': 'Asia', 'Kazakhstan': 'Asia', 'Uzbekistan': 'Asia', 'Afghanistan': 'Asia',
            'Myanmar': 'Asia', 'Sri Lanka': 'Asia', 'Nepal': 'Asia', 'Cambodia': 'Asia',
            'Laos': 'Asia', 'Mongolia': 'Asia', 'North Korea': 'Asia', 'Taiwan': 'Asia',
            'United Arab Emirates': 'Asia', 'Qatar': 'Asia', 'Kuwait': 'Asia', 'Oman': 'Asia',
            'Bahrain': 'Asia', 'Lebanon': 'Asia', 'Jordan': 'Asia', 'Syria': 'Asia',
            'Yemen': 'Asia', 'Palestine': 'Asia', 'Cyprus': 'Asia',
            
            # África
            'Nigeria': 'Africa', 'Ethiopia': 'Africa', 'Egypt': 'Africa', 'South Africa': 'Africa',
            'Algeria': 'Africa', 'Morocco': 'Africa', 'Kenya': 'Africa', 'Tanzania': 'Africa',
            'Uganda': 'Africa', 'Sudan': 'Africa', 'Tunisia': 'Africa', 'Ghana': 'Africa',
            'Zimbabwe': 'Africa', 'Rwanda': 'Africa', 'Senegal': 'Africa', 'Mali': 'Africa',
            'Congo': 'Africa', 'Angola': 'Africa', 'Mozambique': 'Africa', 'Cameroon': 'Africa',
            'Niger': 'Africa', 'Burkina Faso': 'Africa', 'Madagascar': 'Africa', 'Malawi': 'Africa',
            'Ivory Coast': 'Africa', 'Guinea': 'Africa', 'Somalia': 'Africa', 'Zambia': 'Africa',
            'Botswana': 'Africa', 'Namibia': 'Africa', 'Mauritius': 'Africa', 'Libya': 'Africa',
            'Liberia': 'Africa', 'Sierra Leone': 'Africa', 'Togo': 'Africa', 'Benin': 'Africa',
            'Gambia': 'Africa', 'Equatorial Guinea': 'Africa', 'Gabon': 'Africa', 'Eritrea': 'Africa',
            
            # Oceanía
            'Australia': 'Oceania', 'New Zealand': 'Oceania', 'Papua New Guinea': 'Oceania',
            'Fiji': 'Oceania', 'Solomon Islands': 'Oceania', 'Vanuatu': 'Oceania',
            'Samoa': 'Oceania', 'Tonga': 'Oceania'
        }

    async def fetch_csv(self):
        CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"
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
                    for col in self.dataframe.columns:
                        if 'birth' in col.lower() or 'rate' in col.lower():
                            self.dataframe[col] = pd.to_numeric(self.dataframe[col], errors='coerce')
                    
                    # Add continent column based on country
                    country_col = self._get_country_column()
                    if country_col:
                        self.dataframe['Continent'] = self.dataframe[country_col].map(
                            lambda x: self.country_to_continent.get(x, 'Unknown')
                        )
                else:
                    print(f"Error downloading data: {resp.status}")

    def _get_country_column(self):
        """Helper method to identify country column name"""
        possible_names = ['Country', 'Entity', 'Nation', 'Country Name']
        for col in possible_names:
            if col in self.dataframe.columns:
                return col
        return None
    
    def _get_birth_rate_column(self):
        """Helper method to identify birth rate column name"""
        for col in self.dataframe.columns:
            if 'birth' in col.lower() and 'rate' in col.lower():
                return col
        return None

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
        
        birth_rate_col = self._get_birth_rate_column()
        if not birth_rate_col:
            return []
            
        yearly_avg = self.dataframe.groupby('Year')[birth_rate_col].mean().reset_index()
        return yearly_avg.to_dict(orient='records')
    
    async def get_countries_list(self):
        """Returns the list of all countries in the dataset"""
        if self.dataframe.empty:
            return []
        
        country_col = self._get_country_column()
        if not country_col:
            return []
            
        countries = self.dataframe[country_col].unique().tolist()
        return sorted(countries)
    
    async def get_top_countries_by_birth_rate(self, year=None, top_n=10, ascending=False):
        """Returns countries with highest/lowest birth rates for a given year or latest available"""
        if self.dataframe.empty:
            return []
        
        country_col = self._get_country_column()
        birth_rate_col = self._get_birth_rate_column()
        
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
        
        country_col = self._get_country_column()
        birth_rate_col = self._get_birth_rate_column()
        
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
            return []
        
        country_col = self._get_country_column()
        birth_rate_col = self._get_birth_rate_column()
        
        if not country_col or not birth_rate_col:
            return []
        
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
    
    async def get_all_countries_latest_year(self, limit=None):
        """Returns birth rate data for all countries in the latest available year"""
        if self.dataframe.empty:
            return []
        
        country_col = self._get_country_column()
        birth_rate_col = self._get_birth_rate_column()
        
        if not country_col or not birth_rate_col:
            return []
        
        # Get latest year available
        latest_year = self.dataframe['Year'].max()
        
        # Filter data to include only the latest year
        latest_data = self.dataframe[self.dataframe['Year'] == latest_year].copy()
        
        # Group by country and calculate average birth rate
        country_avg = latest_data.groupby(country_col)[birth_rate_col].mean().reset_index()
        
        # Sort by birth rate (highest first)
        country_avg = country_avg.sort_values(birth_rate_col, ascending=False)
        
        # Limit if specified
        if limit:
            country_avg = country_avg.head(limit)
        
        return country_avg.to_dict(orient='records')
    
    async def get_continent_trend(self, continent_name=None):
        """Returns birth rate trend over years for continents"""
        if self.dataframe.empty or 'Continent' not in self.dataframe.columns:
            return []
        
        birth_rate_col = self._get_birth_rate_column()
        if not birth_rate_col:
            return []
        
        # Filter by continent if specified
        if continent_name:
            continent_data = self.dataframe[self.dataframe['Continent'] == continent_name].copy()
        else:
            continent_data = self.dataframe.copy()
        
        # Group by continent and year, calculate average birth rate
        continent_avg = continent_data.groupby(['Continent', 'Year'])[birth_rate_col].mean().reset_index()
        
        # Structure the data for chart consumption
        continents = continent_avg['Continent'].unique().tolist()
        years = sorted(continent_avg['Year'].unique().tolist())
        
        result = {}
        for continent in continents:
            data = continent_avg[continent_avg['Continent'] == continent]
            result[continent] = data[['Year', birth_rate_col]].to_dict(orient='records')
        
        return result
    
    async def get_continents_list(self):
        """Returns the list of all continents in the dataset"""
        if self.dataframe.empty or 'Continent' not in self.dataframe.columns:
            return []
        
        continents = self.dataframe['Continent'].unique().tolist()
        return sorted([c for c in continents if c != 'Unknown'])