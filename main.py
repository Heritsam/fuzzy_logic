import numpy as np
import pandas as pd

from supplier import Supplier

def main():
    f = open('sheets/supplier.csv', 'r')

    suppliers = f.readlines()
    suppliers = suppliers[1:]
    suppliers = [x.strip() for x in suppliers]
    suppliers = [x.split(',') for x in suppliers]
    suppliers = [Supplier(x[0], int(x[1]), int(x[2])) for x in suppliers]

    df = pd.DataFrame([x.to_dict() for x in suppliers])
    df.sort_values(by=['defuzzification'], inplace=True, ascending=False)
    df['qlt_low'] = np.round(df['qlt_low'], 2)
    df['qlt_medium'] = np.round(df['qlt_medium'], 2)
    df['qlt_high'] = np.round(df['qlt_high'], 2)
    df['price_cheap'] = np.round(df['price_cheap'], 2)
    df['price_medium'] = np.round(df['price_medium'], 2)
    df['price_expensive'] = np.round(df['price_expensive'], 2)
    df['bad'] = np.round(df['bad'], 2)
    df['good'] = np.round(df['good'], 2)
    df['excellent'] = np.round(df['excellent'], 2)
    df['defuzzification'] = np.round(df['defuzzification'], 2)

    df.to_excel('sheets/output.xlsx', index=False)
    print(df)

    f.close()

if __name__ == '__main__':
    main()