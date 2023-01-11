
data_dictA = {}
merged_dict = {}
count_A = 1

data_dictB = {}
count_B = 1
#Aの処理---------------------
#1. 自分のデータ作成(key:A, value:sensor_data)
#2. Bのデータ格納
#sensor_dataは順序ラベルもつける
def dictA():
    global count_A
    data = "20221220 000000 00.00"

    counted_data = str(count_A) + "," + data 
    label = "A" + str(count_A)

    data_dictA[label] = counted_data
    count_A += 1

def merge():
    merged_dict = data_dictA | data_dictB
    # for dA in range(len(data_dictA)):
    #     merged_dict.update(str(dA))

    # for dB in range(len(data_dictB)):
    #     merged_dict.update(str(dB))

    print("merged dict↓")
    print(merged_dict)

#----------------------------

#Bの処理---------------------
#1. 自分のデータ作成(key:B, value:sensor_data)
#sensor_dataは順序ラベルもつける
def dictB():
    global count_B
    data = "20221220 000000 00.00"

    counted_data = str(count_B) + "," + data
    label = "B" + str(count_B)

    data_dictB[label] = counted_data
    count_B += 1
#----------------------------

def main():
    for i in range(5):
        dictA()
        dictB()

    print(data_dictA)
    print(data_dictB)

    merge()
        
if __name__ == "__main__":
    main()