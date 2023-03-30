# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:15:36 2023

@author: Arthur
"""
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def main():
    # ========================================================================
    # Funções
    # ========================================================================
    def initDriver():
        s = Service(ChromeDriverManager().install())
        
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=s, options=options)
        return driver
    
    def get_table(xpath):
        table_html = driver.find_elements(by=By.XPATH, value=xpath)[0] \
                                            .get_attribute('outerHTML')
        df = pd.read_html(table_html)[0]
        
        return df
    
    # ========================================================================
    # Inicializando driver
    # ========================================================================
    driver = initDriver()
    
    # ========================================================================
    # Inicializando o dataframe e o mapa das tabelas em HTML
    # ========================================================================
    df = pd.DataFrame(columns=['Nome', 'Categoria', 'Bolsa', 'Ticker', 'Metrica', 'Valor'])
    
    xpath_list = [
        # "/html/body/main/section/div[2]/div/div[1]/h1/div[2]/a",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[1]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[2]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[3]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[4]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[3]/div/div[1]/div[4]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[2]/div[2]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[2]/div[3]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[2]/div[4]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[2]/div[5]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[2]/div[6]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[3]/div/div[2]/div[2]/table",
        "/html/body/main/section/div[4]/div[1]/div[2]/div[3]/div/div[2]/div[3]/table"
        ]
    
    # ========================================================================
    # Iterando sobre todas as URLS
    # ========================================================================
    dict_urls = {
        1: ["nasdaq","aapl", "Apple Inc", "Technology"], 
        2: ["nasdaq","adbe", "Adobe Inc", "Software"],
        3: ["nasdaq","adsk", "Autodesk Inc.", "Software"],
        4: ["nyse","cl", "Colgate-Palmolive Co.", "Household"],
        5: ["nyse","dis", "Walt Disney Co (The)", "Media"],
        6: ["nyse","gis", "General Mills, Inc.", "Packaged Foods & Meats"],
        7: ["nasdaq","googl", "Alphabet Inc", "Internet Services & Infrastructure"],
        8: ["nasdaq","intc", "Intel Corp.", "Semiconductors"],
        9: ["nyse","jnj", "Johnson & Johnson", "Pharmaceuticals"],
        10: ["nyse","k", "Kellogg Co", "Packaged Foods & Meats"],
        11: ["nasdaq","khc", "Kraft Heinz Co", "Packaged Foods & Meats"],
        12: ["nyse","ko", "Coca-Cola Co", "Soft Drinks"],
        13: ["nyse","mcd", "McDonald`s Corp", "Restaurants"],
        14: ["nasdaq","mdlz", "Mondelez International Inc.", "Food Retail"],
        15: ["nyse","mmm", "3M Co.", "Industrial Conglomerates"],
        16: ["nasdq","msft", "Microsoft Corporation", "Internet Services & Infrastructure"],
        17: ["nyse","nke", "Nike, Inc.", "Footwear"],
        18: ["nasdaq","nvda", "NVIDIA Corp", "Semiconductors"],
        19: ["nyse","orcl", "Oracle Corp.", "Internet Services & Infrastructure"],
        20: ["nasdaq","pep", "PepsiCo Inc", "Soft Drinks"],
        21: ["nyse","pg", "Procter & Gamble Co.", "Household & Personal Products"],
        22: ["nyse","schw", "Charles Schwab Corp.", "Capital Markets"],
        23: ["nyse","swk", "Stanley Black & Decker Inc", "Electrical Components & Equipment"],
        24: ["nyse","t", "AT&T, Inc.", "Telecommunication Services"],
        25: ["nyse","ul", "Unilever plc", "Household & Personal Products"],
        26:["nasdaq", "asml", "ASML Holding NV", 'Semiconductor Equipment'],
        27:["nasdaq", "amzn", "Amazon.com Inc.", "Specialty Retail"],
        28:["nyse", "mrk", "Merck & Co Inc","Pharmaceuticals"],
        29:["nyse", "pfe", "Pfizer Inc.", "Pharmaceuticals"],
        30:["nyse", "v", "Visa Inc", "Consumer Finance"],
        31:["nyse", "crm", "Salesforce Inc", "Application Software"],
        32:["nyse", "slb", "Schlumberger", "Oil & Gas Equipment & Services"],
        33:["nyse", "cvx", "Chevron Corp.", "Integrated Oil & Gas"],
        34:["nyse", "whd", "Cactus Inc", "Oil & Gas Equipment & Services"],
    }
    
    for key in dict_urls:
        # break
        categoria = dict_urls[key][3]
        nome = dict_urls[key][2]
        bolsa = dict_urls[key][0]
        ticker = dict_urls[key][1]
    
        print(ticker)
        
        url = f"https://wallmine.com/{bolsa}/{ticker}"
        
        driver.get(url)
    
    
        # ====================================================================
        # Loop em todas as tabelas da página
        # ====================================================================
        for xpath in xpath_list:
            # break
            # Adicionando linhas da tabela no dataframe
            temp_df = get_table(xpath)
            
            # Adicionando Bolsa e Ticker
            temp_df.insert(0, 'Ticker', ticker)
            temp_df.insert(0, 'Bolsa', bolsa)
            temp_df.insert(0, 'Categoria', categoria)
            temp_df.insert(0, 'Nome', nome)
            
    
            # Loop para adicionar linhas do df1 ao df2
            for i in range(len(temp_df)):
                df.loc[len(df)] = temp_df.iloc[i].values
                     
    # ========================================================================
    # Salvando RAW   
    # ========================================================================
    df.to_csv("./dataset/RAW.csv", index=False, sep=";")   
    # df = pd.read_csv("RAW.csv", sep=";")    
    
    # ========================================================================
    # Pré tratamento dos valores e métricas    
    # ======================================================================== 
    df['Valor'] = df['Valor'].fillna(0)
    df['Metrica'] = df['Metrica'].apply(lambda x: str(x).strip())
    
    # ========================================================================
    # Eliminando algumas métricas
    # ========================================================================
    mask = ['Short % of float', 
            'Shares float',
            'Earnings date',
            'Ex-dividend date',
            'Payment date']
    
    # mask = ['Enterprise value']
    
    mask_bool = df['Metrica'].isin(mask)
    df = df[~mask_bool]
    
    # ========================================================================
    # Limpando valores financeiros e colocando todos em Bilhao
    # ========================================================================
    def fLimpadora(x):
        x = str(x)
        old_x = x
        try: 
            if '$' in x:
                x = x.replace('$', '')
            elif '€' in x:
                x = x.replace('€', '')
                
            if 'T' in x:
                x = x.replace('T', '')
                x = float(x)
                x = int(x * 10**12)
            elif 'B' in x:
                x = x.replace('B', '')
                x = float(x)
                x = int(x * 10**9)
            elif 'M' in x:
                x = x.replace('M', '')
                x = float(x)
                x = int(x * 10**6)
            elif 'k' in x:
                x = x.replace('k', '')
                x = float(x)
                x = int(x * 10**3)
            elif '%' in x:
                x = x.replace('%', '')
        except:
            return old_x
        
        try: 
            x = float(x)
        except:
            return old_x
        
        return x   
    
    df['Valor']= df['Valor'].apply(fLimpadora)
    
    # ========================================================================
    # Salvando Base   
    # ========================================================================
    df.to_csv("./dataset/Base.csv", index=False, sep=";", encoding='UTF-8')   

if __name__ == '__main__':
    main()