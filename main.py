from bal_pars.init_login import start_pars, try_login
from bal_pars.cvs_point import init_csv



def main():
    try_login()
    init_csv()
    for code in ["00", "1010400072", "1010400083", ]:
        start_pars(code)
    

if __name__ == "__main__":
    main()