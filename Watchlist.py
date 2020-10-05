import pandas as pd


def watchlist():
    try:
        watching = pd.read_csv("watching.csv", index_col = [0])
    except:
        watching = pd.DataFrame(columns = ['company', 'C/P', 'Exp', 'Target','Paid'])
    print(watching)
    while input("Do you want to add an option to your watchlist? (Y/N) ") == "Y":
        company = input("Enter Company Name: ")
        CallPut = input("Enter Call or Put: ")
        Exp_date = input("Enter Expiration Date (mm/dd/yy): ")
        Target = float(input("Enter Target Price: "))
        Paid = float(input("Enter Amount Paid: "))
        Strike = float(input("Enter Strike Price: "))
        watching = watching.append({'company': company, "C/P": CallPut, "Exp":Exp_date, "Target":Target, "Paid":Paid, "Strike":Strike}, ignore_index = True)


    watching.to_csv("watching.csv")
    return(watching)
