# +: 1
# -: 0
# 1: 1
# 0: 0
# X
# Z
import random
import numpy as np

qubit = ['|+>', '|->', '|0>', '|1>']
bit = ['0', '1']
measurement = ['X', 'Z']
x_measure = ['|+>', '|->']
z_measure = ['|0>', '|1>']

def Alice_qubit_seq(qubit_length):
    # Alice制备一组偏振态光子
    qubit_seq = []
    for i in range(qubit_length):
        qubit_seq.append(qubit[random.randint(0, 3)])

    return qubit_seq


def random_measurement_seq(qubit_length):
    m_seq = []
    for i in range(qubit_length):
        m_seq.append(measurement[random.randint(0, 1)])

    return m_seq


def from_qubit_to_bit(qubit_seq):
    # qubit is a list
    # return bit sequence
    bit_seq = []
    for qubit in qubit_seq:
        if qubit == '|+>':
            bit_seq.append('1')
        if qubit == '|->':
            bit_seq.append('0')
        if qubit == '|0>':
            bit_seq.append('0')
        if qubit == '|1>':
            bit_seq.append('1')

    return bit_seq

def measure(qubit_seq, measurement_seq):
    if len(qubit_seq) != len(measurement_seq):
        print('测量出错，量子比特序列长度和测量基序列长度不一致，exiting...')
        exit(0)

    l = len(qubit_seq)
    result_qubit_seq = []

    p = np.array([0.5, 0.5])

    for i in range(l):
        if qubit_seq[i] == '|->'and measurement_seq[i] == 'X':
            result_qubit_seq.append(qubit_seq[i])
        if qubit_seq[i] == '|+>' and measurement_seq[i] == 'X':
            result_qubit_seq.append(qubit_seq[i])
        if qubit_seq[i] == '|0>' and measurement_seq[i] == 'Z':
            result_qubit_seq.append(qubit_seq[i])
        if qubit_seq[i] == '|1>' and measurement_seq[i] == 'Z':
            result_qubit_seq.append(qubit_seq[i])

        if qubit_seq[i] == '|0>' and measurement_seq[i] == 'X':
            # 指定概率取样，0.5+0.5
            np.random.seed(0)
            result_qubit_seq.append(np.random.choice(x_measure, p=p.ravel()))
        if qubit_seq[i] == '|1>' and measurement_seq[i] == 'X':
            np.random.seed(0)
            result_qubit_seq.append(np.random.choice(x_measure, p=p.ravel()))
        if qubit_seq[i] == '|+>' and measurement_seq[i] == 'Z':
            np.random.seed(0)
            result_qubit_seq.append(np.random.choice(z_measure, p=p.ravel()))
        if qubit_seq[i] == '|->' and measurement_seq[i] == 'Z':
            np.random.seed(0)
            result_qubit_seq.append(np.random.choice(z_measure, p=p.ravel()))

    return result_qubit_seq


def Alice_find_correct_measure(alice_qubit_seq, bob_measure_seq):
    global x_measure, z_measure

    l = len(alice_qubit_seq)
    correct = []
    for i in range(l):
        if alice_qubit_seq[i] in x_measure and bob_measure_seq[i] == 'X':
            correct.append(i)
        if alice_qubit_seq[i] in z_measure and bob_measure_seq[i] == 'Z':
            correct.append(i)

    return correct


def get_key(correct, bit_seq):
    key = []
    for i in correct:
        key.append(bit_seq[i])
    return key

def calc_error_rate(half_key1, half_key2):
    # half_key2 is real
    l = len(half_key1)
    error = 0
    for i in range(l):
        if half_key1[i] != half_key2[i]:
            error += 1

    return error/l


def bb84_main(qubit_length):
    # qubit_length = int(input('请输入发送方Alice制备的一组偏振态光子的长度：'))

    # Alice制备一组偏振态光子
    alice_qubit_seq = Alice_qubit_seq(qubit_length)
    print('ALICE制备的偏振态光子序列：', alice_qubit_seq)

    # Alice这组偏振态光子的比特值
    alice_bit_seq = from_qubit_to_bit(alice_qubit_seq)
    print('ALICE的比特值序列：', alice_bit_seq)

    # # 1个Eve在窃听
    # eve_measure_seq = random_measurement_seq(qubit_length)
    # print('EVE选择的测量基：', eve_measure_seq)
    #
    # eve_qubit_seq = measure(alice_qubit_seq, eve_measure_seq)
    # print('EVE的偏振态光子的测量结果：', eve_qubit_seq)
    #
    # # Eve这组偏振态光子的比特值
    # eve_bit_seq = from_qubit_to_bit(eve_qubit_seq)
    # # print('BOB的比特值序列：', eve_bit_seq)

    # Bob随机选择测量基
    bob_measure_seq = random_measurement_seq(qubit_length)
    print('选择的测量基：', bob_measure_seq)

    # Bob用测量基测量，得到Bob的测量结果
    bob_qubit_seq = measure(alice_qubit_seq, bob_measure_seq)
    print('BOB的偏振态光子的测量结果：', bob_qubit_seq)

    # Bob这组偏振态光子的比特值
    bob_bit_seq = from_qubit_to_bit(bob_qubit_seq)
    print('BOB的比特值序列：', bob_bit_seq)

    print('BOB通过经典信道告诉ALICE选择的测量基：', bob_measure_seq)

    correct = Alice_find_correct_measure(alice_qubit_seq, bob_measure_seq)
    print('ALICE 告诉 BOB 保留那些测量结果：', correct)

    bob_key = ''.join(get_key(correct, bob_bit_seq))
    print('BOB KEY: ', bob_key)

    alice_key = ''.join(get_key(correct, alice_bit_seq))
    print('ALICE KEY: ', alice_key)

    # eve_key = ''.join(get_key(correct, eve_bit_seq))
    # # print('EVE KEY: ', eve_key)

    # BOB ALICE 公布key的前半部分
    bob_publish_half_key = bob_key[:int(len(bob_key)/2)]
    alice_publish_half_key = alice_key[:int(len(alice_key)/2)]
    # print(bob_publish_half_key, alice_publish_half_key)

    # 计算误码率
    error_rate = calc_error_rate(bob_publish_half_key, alice_publish_half_key)
    print('BOB KEY的误码率：', error_rate)

    return error_rate

max_eve_number = 10

def multiple_eves(qubit_length):

    # Alice制备一组偏振态光子
    alice_qubit_seq = Alice_qubit_seq(qubit_length)
    # print('ALICE制备的偏振态光子序列：', alice_qubit_seq)

    # Alice这组偏振态光子的比特值
    alice_bit_seq = from_qubit_to_bit(alice_qubit_seq)
    # print('ALICE的比特值序列：', alice_bit_seq)

    rate = []

    for eve_number in range(max_eve_number):
        # print('一共有'+ str(eve_number)+'个人在窃听...')

        for time in range(0, eve_number+1):
            if time == 0:
                eve_measure_seq = random_measurement_seq(qubit_length)
                # print('EVE选择的测量基：', eve_measure_seq)

                eve_qubit_seq = measure(alice_qubit_seq, eve_measure_seq)
                # print('EVE的偏振态光子的测量结果：', eve_qubit_seq)

                # Eve这组偏振态光子的比特值
                eve_bit_seq = from_qubit_to_bit(eve_qubit_seq)
                # print('BOB的比特值序列：', eve_bit_seq)
            else:
                eve_measure_seq = random_measurement_seq(qubit_length)
                # print('EVE选择的测量基：', eve_measure_seq)

                eve_qubit_seq = measure(eve_qubit_seq, eve_measure_seq)
                # print('EVE的偏振态光子的测量结果：', eve_qubit_seq)

                # Eve这组偏振态光子的比特值
                eve_bit_seq = from_qubit_to_bit(eve_qubit_seq)
                # print('BOB的比特值序列：', eve_bit_seq)

        # 循环里的最后一个“EVE”就是BOB
        correct = Alice_find_correct_measure(alice_qubit_seq, eve_measure_seq)
        # print('ALICE 告诉 BOB 保留那些测量结果：', correct)

        key = ''.join(get_key(correct, eve_bit_seq))
        # print('KEY: ', bob_key)

        alice_key = ''.join(get_key(correct, alice_bit_seq))
        # print('ALICE KEY: ', alice_key)

        # BOB ALICE 公布key的前半部分
        publish_half_key = key[:int(len(key)/2)]
        alice_publish_half_key = alice_key[:int(len(alice_key)/2)]
        # print(bob_publish_half_key, alice_publish_half_key)

        # 计算误码率
        error_rate = calc_error_rate(publish_half_key, alice_publish_half_key)
        # print('KEY的误码率：', error_rate)
        rate.append(error_rate)

    return rate





import matplotlib.pyplot as plt

if __name__ == '__main__':
    bb84_main(9)

    # print('ONE EVE IS LISTENING...')
    #
    # rates = []
    # for qubit_length in range(10, 10000):
    #     error_rate = bb84_main(qubit_length)
    #     rates.append(error_rate)
    #
    # plt.scatter(range(10, 10000), rates, marker='.', c='olive')
    # plt.xlabel('Alice qubits\' length')
    # plt.ylabel('Error rate')
    # plt.show()

    # rates = {}
    # for eve_number in range(max_eve_number):
    #     rates[eve_number] = []
    #
    # for qubit_length in range(20, 1000):
    #     # 一个量子比特串的长度 对应多种（0-9）EVE窃听的情况
    #     multiple_rate = multiple_eves(qubit_length)
    #     # max_eve_number = len(rates)
    #     for i in range(len(multiple_rate)):
    #         rates[i].append(multiple_rate[i])
    #
    # # print(rates)
    # np.save('20-1000_rates.npy', rates)
    #
    # # # Load
    # # read_dictionary = np.load('my_file.npy').item()
    # # print(read_dictionary['hello']) # displays "world"
    #
    # colors = ['olive', 'firebrick', 'orange', 'dodgerblue', 'orchid', 'slategrey', 'rosybrown', 'seagreen', 'violet', 'deeppink']
    # for number in range(max_eve_number):
    #     plt.scatter(range(20, 1000), rates[number], marker='.', c=colors[number], label=str(number))
    #     plt.xlabel('Alice qubits\' length')
    #     plt.ylabel('Error rate')
    #     plt.legend()
    #     plt.figure()
    #
    # # plt.xlabel('Alice qubits\' length')
    # # plt.ylabel('Error rate')
    # # plt.legend()
    # plt.show()
    #
    #

