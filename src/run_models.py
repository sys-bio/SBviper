import os

directory = "/Users/mabochen/Desktop/Research/km_test/examples/biomodels"

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        print(filename)
        os.system("python3 main_runner.py ../examples/biomodels/" + filename + " >> ../examples/biomodels_report/" +
                  os.path.splitext(filename)[0] + "_report.txt")
