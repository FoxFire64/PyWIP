import quandl
from key import *


def stock_print(stock, success):
    """ Takes in user-chosen stock and, if valid,
        displays the Stock's head data in the dataframe """
    try:
        df = quandl.get(stock)

        '''Here we set the head to mainly include the Adjusted Open,
            Adjusted High, Adjusted Low, Adjusted Close, and Adjusted Volume.
            This is the data we'll work with to define the predictive data'''
        df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume']]

        # High-Low Percent = (High - Low) / Low * 100
        df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] * 100.0

        # Percent Change = (Daily Close - Daily Open) / Daily Open * 100
        df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

        # Now the head we're working with will be Close, HL_PCT, PCT_change, and Volume
        df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

        # Print the head
        print(df.head())
        return True
    except SyntaxError:
        print("\"%s\" must be in the format DATABASE_CODE/DATASET_CODE" % stock)


def main():
    quandl.ApiConfig.api_key = akey
    success = False
    while not success:
        stock = raw_input("What stock do you want to look at? ").upper()
        success = stock_print(stock, success)


if __name__ == '__main__':
    main()
