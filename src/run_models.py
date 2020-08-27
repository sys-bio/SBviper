import os

directory = "/Users/mabochen/Desktop/Research/km_test/examples/biomodels"

for filename in os.listdir(directory):
    i = 0
    if filename.endswith(".xml"):
        os.system("python3 main_runner.py ../examples/biomodels/" + filename + " >> ../examples/biomodels_report/" +
                  os.path.splitext(filename)[0] + "_report.txt")
