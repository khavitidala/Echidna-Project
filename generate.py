"""
Program untuk membuat tabel waktu eksekusi
algoritma selection dan insertion beserta grafiknya
"""
import time 
import random
import xlwt 
import matplotlib.pyplot as plt
import threading

from xlwt import Workbook



A = [64, 25, 12, 22, 11] 

def selectionSort(A):
    start = time.perf_counter()
    for i in range(len(A)): 
        min_idx = i 
        for j in range(i+1, len(A)): 
            if A[min_idx] > A[j]: 
                min_idx = j        
        A[i], A[min_idx] = A[min_idx], A[i] 
    finish = time.perf_counter()
    return round(finish-start, 10)
  
def insertionSort(arr): 
    start = time.perf_counter()
    for i in range(1, len(arr)): 
        key = arr[i] 
        j = i-1
        while j >=0 and key < arr[j] : 
            arr[j+1] = arr[j] 
            j -= 1
        arr[j+1] = key 
    finish = time.perf_counter()
    return round(finish-start, 10)

def generate_data(min, max, seed, y):
    result = {}
    random.seed(seed)
    i = min
    while (i <= max):
        data = [random.randint(min, max) for _ in range(min, i+1)]
        result[i] = {"selection": selectionSort(data), "insertion": insertionSort(data)}
        i+=y
    return result

def simpan_excel(dict_data, wb):
    sheet1 = wb.add_sheet("Running Time")
    sheet1.write(0,0, "Jumlah n")
    sheet1.write(0,1, "Selection (sec)")
    sheet1.write(0,2, "Insertion (sec)")
    i=0
    for key, value in dict_data.items():
        sheet1.write(1+i,0, key)
        sheet1.write(1+i,1, "{:.10f}".format(value["selection"])) 
        sheet1.write(1+i,2, "{:.10f}".format(value["insertion"]))
        i += 1
    wb.save('runningtime.xls')

def plotting(dict_data):
    xaxis = []
    ysel = []
    yins = []
    for k,v in dict_data.items():
        xaxis.append(k)
        ysel.append(v["selection"])
        yins.append(v["insertion"])
    fig, ax = plt.subplots()
    ax.set(title = 'Perbedaan Running Time Selection dan Insertion Sort',
            xlabel= 'Jumlah data (n)',
            ylabel= 'Waktu eksekusi (detik)')
    ax.yaxis.grid()
    plt.plot(xaxis, ysel, label="Selection")
    plt.plot(xaxis, yins, label="Insertion")
    plt.legend()
    plt.savefig('runtime.png')
    #plt.show()
start = time.perf_counter()
wb = Workbook()
min = int(input("Masukkan angka minimal jumlah inputan: "))
x = int(input("Masukkan angka maksimal jumlah inputan: "))
y = int(input("Masukkan range antar misal 10, maka data yg dipakai adalah kelipatan 10: "))
seed = int(input("Masukkan satu angka integer (bebas) untuk insialisasi random.seed:  "))
data = generate_data(min, x, seed, y)
print("Harap tunggu, program sedang membuat file yang anda butukan...")
simpan_excel(data, wb)
plotting(data)
finish = time.perf_counter()
print(f"Data berhasil disimpan dalam {round(finish-start, 5)}")