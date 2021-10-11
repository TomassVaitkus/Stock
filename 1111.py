from pyfinviz.screener import Screener

# with no params (default screener table)
screener = Screener()
# with params (The first 3 pages of "STOCKS ONLY" where Analyst recommend a strong buy)

options = [Screener.IndustryOption.STOCKS_ONLY_EX_FUNDS, Screener.AnalystRecomOption.STRONG_BUY_1]
screener = Screener(filter_options=options, view_option=Screener.ViewOption.OVERVIEW,
                    pages=[x for x in range(1, 5)])

# available variables:
# print(screener.main_url)  # scraped URL
# print(screener.soups)  # beautiful soup object per page {1: soup, 2: soup, ...}
print(screener.data_frames[2])  # table information in a pd.DataFrame object per page {1: table_df, 2, table_df, ...}
