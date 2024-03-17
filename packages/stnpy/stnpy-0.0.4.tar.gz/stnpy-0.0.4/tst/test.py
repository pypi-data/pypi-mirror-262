from stnpy import stn

if __name__ == '__main__':
    for i in range(10):
        print(stn.run_file(filename="resources/stn.csv", delimiter=",", best_fit=0, run_number=i + 1))
