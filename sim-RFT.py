from __future__ import division
import numpy as np
import random
import time
import datetime
#import matplotlib.pyplot as plt
from collections import defaultdict
#from PIL import Image
from TOA import *
import os.path
import math
import os


# Sim-RFT Configuration values
RANDOM = 'RANDOM'
BURST = 'BURST'
# Fragment error rate (Random probability) FER % -> 10 %
FER_RANDOM = 1
# Burst Occurrance Probability (probability to enter a burst) BOP * 100 = % example 0.01 * 100 = 1%
FER = 0.01
# Repetitions to calculate Poisson distributions
poisson_repetitions = 10000000
# Burst length (lamba) value
poisson_lambda = 10
# Bitmap generation mode
BITMAP_GENERATION = RANDOM
# Size of FN for the List of Lost Fragments
list_of_fragments_numbers_lenght = 7 #bits
# Min bitmap size in simulation
bitmap_size = 2
# Max bitmap size in simulation
bitmap_size_max = 140
# delta in simulation
bitmap_delta = 1
# Number of simulations
repetitions = 1000000
# LoRa Payload size (frame size - ack headers)
# frame size = 11 bytes, ACK headers = 1 byte
LORA_PAYLOAD = 10
SIGFOX_PAYLOAD = 11
# Configuration values
PRINT_PDF = False
SHOW_BITMAP_IMAGE = False
SHOW_POISSON_GRAPH = False
SHOW_BURST_GRAPH = False
WRITE_TO_file = True
PRINT_ALL = False
# repetitions = 10


# Save path for output files
save_path = 'graphs/'

script_dir = os.path.dirname(__file__)
save_path = os.path.join(script_dir, save_path)

#Variables for TOA results
list_of_deltas_sdnv_2_results_TOA = defaultdict(float)
list_of_deltas_sdnv_3_results_TOA = defaultdict(float)
list_of_deltas_sdnv_4_results_TOA = defaultdict(float)
list_of_deltas_sdnv_5_results_TOA = defaultdict(float)
list_of_fragments_numbers_results_TOA = defaultdict(float)
compressed_bitmap_results_TOA = defaultdict(float)
bitmap_results_TOA = defaultdict(float)
#Variables for ToA probability of occurrence
list_of_deltas_sdnv_2_results_TOA_prob = defaultdict(float)
list_of_deltas_sdnv_3_results_TOA_prob = defaultdict(float)
list_of_deltas_sdnv_4_results_TOA_prob = defaultdict(float)
list_of_deltas_sdnv_5_results_TOA_prob = defaultdict(float)
list_of_fragments_numbers_results_TOA_prob = defaultdict(float)
compressed_bitmap_results_TOA_prob = defaultdict(float)
bitmap_results_TOA_prob = defaultdict(float)
#Variables for ToA probability density function
list_of_deltas_sdnv_2_results_TOA_pdf = defaultdict(float)
list_of_deltas_sdnv_3_results_TOA_pdf = defaultdict(float)
list_of_deltas_sdnv_4_results_TOA_pdf = defaultdict(float)
list_of_deltas_sdnv_5_results_TOA_pdf = defaultdict(float)
list_of_fragments_numbers_results_TOA_pdf = defaultdict(float)
compressed_bitmap_results_TOA_pdf = defaultdict(float)
bitmap_results_TOA_pdf = defaultdict(float)

#Variables for ToA variance
list_of_deltas_sdnv_2_results_TOA_variance = defaultdict(float)
list_of_deltas_sdnv_3_results_TOA_variance = defaultdict(float)
list_of_deltas_sdnv_4_results_TOA_variance = defaultdict(float)
list_of_deltas_sdnv_5_results_TOA_variance = defaultdict(float)
list_of_fragments_numbers_results_TOA_variance = defaultdict(float)
compressed_bitmap_results_TOA_variance = defaultdict(float)
bitmap_results_TOA_variance = defaultdict(float)

#Variables for ToA standard deviation sd
list_of_deltas_sdnv_2_results_TOA_sd = defaultdict(float)
list_of_deltas_sdnv_3_results_TOA_sd = defaultdict(float)
list_of_deltas_sdnv_4_results_TOA_sd = defaultdict(float)
list_of_deltas_sdnv_5_results_TOA_sd = defaultdict(float)
list_of_fragments_numbers_results_TOA_sd = defaultdict(float)
compressed_bitmap_results_TOA_sd = defaultdict(float)
bitmap_results_TOA_sd = defaultdict(float)

def average_calculation(info_dic):
    #print info_dic
    average = 0
    provisional = 0
    provisional2 = 0
    for i in info_dic:
        provisional = provisional + info_dic[i] * i
        provisional2 = provisional2 + info_dic[i]
        #print "provisional: " + str(provisional)
        #print "provisionsal2: " + str(provisional2)
    average = provisional / provisional2
    return average
def variance_calculation(info_dic):
    sum_of_numbers = sum(number*count for number, count in info_dic.iteritems())
    count = sum(count for n, count in info_dic.iteritems())
    print sum_of_numbers
    print count
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in info_dic.iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    return variance

def sd_calculation(info_dic):
    sum_of_numbers = sum(number*count for number, count in info_dic.iteritems())
    count = sum(count for n, count in info_dic.iteritems())
    print sum_of_numbers
    print count
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in info_dic.iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    return std_dev


def pdf_calculation(info_dic, repetitions):
    '''Obtain average value of info_dic'''
    temp_dic = defaultdict(float)
    for i in info_dic:
        temp_dic[i] = (info_dic[i]/repetitions)
    return temp_dic

def frames_calculation(payload_size, results_dic):
    '''Calculate the number of frames considering the payload size
    payload size = frame size - ack header '''
    framesResults = defaultdict(float)
    #print results_dic
    #print 'Frame calculation'
    '''FRAME CALCULATION FOR COMPRESSED BITMAP'''
    for i in results_dic:
        #LORA FRAMES
        if i == 0:
            framesResults[1] += results_dic[i]
        elif i <= payload_size:
            framesResults[1] += results_dic[i]
        elif i <= 2*payload_size:
            framesResults[2] += results_dic[i]
        elif i <= 3*payload_size:
            framesResults[3] += results_dic[i]
        elif i <= 4*payload_size:
            framesResults[4] += results_dic[i]
        elif i <= 5*payload_size:
            framesResults[5] += results_dic[i]
        elif i <= 6*payload_size:
            framesResults[6] += results_dic[i]
        elif i <= 7*payload_size:
            framesResults[7] += results_dic[i]
        elif i <= 8*payload_size:
            framesResults[8] += results_dic[i]
        elif i <= 9*payload_size:
            framesResults[9] += results_dic[i]    
        elif i <= 10*payload_size:
            framesResults[10] += results_dic[i]
    return framesResults
    





print 'FER -> ' + str(FER*100) + '%'
print 'RANDOM FER -> ' + str(FER_RANDOM) + '%'
print 'poisson_lambda -> ' + str(poisson_lambda)
print "BITMAP_GENERATION = "+  BITMAP_GENERATION
print 'list_of_fragments_numbers_lenght = ' + str(list_of_fragments_numbers_lenght) 
print 'bitmap_size = ' + str(bitmap_size)
print 'bitmap_size_max = ' + str(bitmap_size_max)
print 'bitmap_delta = ' + str(bitmap_delta)
print 'repetitions =' + str(repetitions) 

'''Variables for results of different ack methods'''

#FRAMES VARIABLES

list_of_deltas_sdnv_2_results_frames_lora = defaultdict(float)
list_of_deltas_sdnv_3_results_frames_lora = defaultdict(float)
list_of_deltas_sdnv_4_results_frames_lora = defaultdict(float)
list_of_deltas_sdnv_5_results_frames_lora = defaultdict(float)
list_of_fragments_numbers_results_frames_lora = defaultdict(float)
compressed_bitmap_results_frames_lora = defaultdict(float)
bitmap_results_frames_lora = defaultdict(float)

list_of_deltas_sdnv_2_results_frames_lora_prob = defaultdict(float)
list_of_deltas_sdnv_3_results_frames_lora_prob = defaultdict(float)
list_of_deltas_sdnv_4_results_frames_lora_prob = defaultdict(float)
list_of_deltas_sdnv_5_results_frames_lora_prob = defaultdict(float)
list_of_fragments_numbers_results_frames_lora_prob = defaultdict(float)
compressed_bitmap_results_frames_lora_prob = defaultdict(float)
bitmap_results_frames_lora_prob = defaultdict(float)

list_of_deltas_sdnv_2_results_frames_lora_pdf = defaultdict(float)
list_of_deltas_sdnv_3_results_frames_lora_pdf = defaultdict(float)
list_of_deltas_sdnv_4_results_frames_lora_pdf = defaultdict(float)
list_of_deltas_sdnv_5_results_frames_lora_pdf = defaultdict(float)
list_of_fragments_numbers_results_frames_lora_pdf = defaultdict(float)
compressed_bitmap_results_frames_lora_pdf = defaultdict(float)
bitmap_results_frames_lora_pdf = defaultdict(float)

list_of_deltas_sdnv_2_results_frames_lora_variance = defaultdict(float)
list_of_deltas_sdnv_3_results_frames_lora_variance = defaultdict(float)
list_of_deltas_sdnv_4_results_frames_lora_variance = defaultdict(float)
list_of_deltas_sdnv_5_results_frames_lora_variance = defaultdict(float)
list_of_fragments_numbers_results_frames_lora_variance = defaultdict(float)
compressed_bitmap_results_frames_lora_variance = defaultdict(float)
bitmap_results_frames_lora_variance = defaultdict(float)

list_of_deltas_sdnv_2_results_frames_lora_sd = defaultdict(float)
list_of_deltas_sdnv_3_results_frames_lora_sd = defaultdict(float)
list_of_deltas_sdnv_4_results_frames_lora_sd = defaultdict(float)
list_of_deltas_sdnv_5_results_frames_lora_sd = defaultdict(float)
list_of_fragments_numbers_results_frames_lora_sd = defaultdict(float)
compressed_bitmap_results_frames_lora_sd = defaultdict(float)
bitmap_results_frames_lora_sd = defaultdict(float)


list_of_fragments_numbers_result = defaultdict(float)
optimizedBitmap_summary = defaultdict(float)
list_of_fragments_numbers_result_summary = defaultdict(float)
Bitmap_summary = defaultdict(float)

optimizedBitmap_summary_variance = defaultdict(float)
optimizedBitmap_summary_sd = defaultdict(float)
Bitmap_summary_variance = defaultdict(float)
Bitmap_summary_sd = defaultdict(float)
list_of_fragments_numbers_result_summary_variance = defaultdict(float)
list_of_fragments_numbers_result_summary_sd = defaultdict(float)

list_of_deltas_results_sdnv_2 = defaultdict(float)
list_of_deltas_results_sdnv_3 = defaultdict(float)
list_of_deltas_results_sdnv_4 = defaultdict(float)
list_of_deltas_results_sdnv_5 = defaultdict(float)

list_of_deltas_results_summary_sdnv_2 = defaultdict(float)
list_of_deltas_results_summary_sdnv_3 = defaultdict(float)
list_of_deltas_results_summary_sdnv_4 = defaultdict(float)
list_of_deltas_results_summary_sdnv_5 = defaultdict(float)

list_of_deltas_results_summary_sdnv_2_variance = defaultdict(float)
list_of_deltas_results_summary_sdnv_3_variance = defaultdict(float)
list_of_deltas_results_summary_sdnv_4_variance = defaultdict(float)
list_of_deltas_results_summary_sdnv_5_variance = defaultdict(float)

list_of_deltas_results_summary_sdnv_2_sd = defaultdict(float)
list_of_deltas_results_summary_sdnv_3_sd = defaultdict(float)
list_of_deltas_results_summary_sdnv_4_sd = defaultdict(float)
list_of_deltas_results_summary_sdnv_5_sd = defaultdict(float)


list_of_deltas_results_summary_bits_sdnv_2 = defaultdict(float)
list_of_deltas_results_summary_bits_sdnv_3 = defaultdict(float)
list_of_deltas_results_summary_bits_sdnv_4 = defaultdict(float)
list_of_deltas_results_summary_bits_sdnv_5 = defaultdict(float)

list_of_deltas_results_bytes_sdnv_2  = defaultdict(float)
list_of_deltas_results_bytes_sdnv_3  = defaultdict(float)
list_of_deltas_results_bytes_sdnv_4  = defaultdict(float)
list_of_deltas_results_bytes_sdnv_5  = defaultdict(float)

list_of_deltas_results_bits_sdnv_2  = defaultdict(float)
list_of_deltas_results_bits_sdnv_3  = defaultdict(float)
list_of_deltas_results_bits_sdnv_4  = defaultdict(float)
list_of_deltas_results_bits_sdnv_5  = defaultdict(float)

list_of_deltas_results_summary_bytes_sdnv_2 = defaultdict(float)
list_of_deltas_results_summary_bytes_sdnv_3 = defaultdict(float)
list_of_deltas_results_summary_bytes_sdnv_4 = defaultdict(float)
list_of_deltas_results_summary_bytes_sdnv_5 = defaultdict(float)

list_of_deltas_results_summary_bytes_probability_sdnv_2 = defaultdict(float)
list_of_deltas_results_summary_bytes_probability_sdnv_3 = defaultdict(float)
list_of_deltas_results_summary_bytes_probability_sdnv_4 = defaultdict(float)
list_of_deltas_results_summary_bytes_probability_sdnv_5 = defaultdict(float)

list_of_deltas_real_results_summary_bits_sdnv_2 = defaultdict(float)
list_of_deltas_real_results_summary_bits_sdnv_3 = defaultdict(float)
list_of_deltas_real_results_summary_bits_sdnv_4 = defaultdict(float)
list_of_deltas_real_results_summary_bits_sdnv_5 = defaultdict(float)

list_of_deltas_results_bits = defaultdict(float)
list_of_fragments_numbers_result_bits = defaultdict(float)
optimizedBitmap_summary_bits = defaultdict(float)
list_of_deltas_results_summary_bits = defaultdict(float)
list_of_fragments_numbers_result_summary_bits = defaultdict(float)
Bitmap_summary_bits = defaultdict(float)

list_of_deltas_results_bytes = defaultdict(float)
list_of_fragments_numbers_result_bytes = defaultdict(float)
optimizedBitmap_summary_bytes = defaultdict(float)
list_of_deltas_results_summary_bytes = defaultdict(float)
list_of_fragments_numbers_result_summary_bytes = defaultdict(float)
Bitmap_summary_bytes = defaultdict(float)

optimizedBitmap_summary_bytes_probability = defaultdict(float)
list_of_deltas_results_summary_bytes_probability = defaultdict(float)
list_of_fragments_numbers_result_summary_bytes_probability = defaultdict(float)
Bitmap_summary_bytes_probability = defaultdict(float)

probability_total_results = defaultdict(float)
burst_size_total_results = defaultdict(float)
burst_size_real_total_results = defaultdict(float)

probability_total_summary = defaultdict(float)
burst_size_total_summary = defaultdict(float)
burst_size_real_total_summary = defaultdict(float)
burst_prob_apparence = defaultdict(float)

list_of_deltas_real_results_summary_bits = defaultdict(float)

'''Variables and poisson calculation'''
counted = defaultdict(float)
probability_poisson = defaultdict(float)
if BITMAP_GENERATION == BURST:
    print 'Calculating poisson ' + str(poisson_repetitions)
    probability = np.random.poisson(poisson_lambda,poisson_repetitions)

    for i,v in enumerate(probability):
        counted[v] += 1

    print len(probability)
    for i in counted:
        print str(i)+',' + str(counted[i]) +','+ str(counted[i]/len(probability))
        probability_poisson[i] = counted[i]/len(probability)

    print counted
    print probability_poisson
    probability_sum = defaultdict(float)
    for i in counted:
        if i == 0:
            print '0'
            probability_sum[i] = counted[i]
        else:
            probability_sum[i] = probability_sum[i-1] + counted[i]
            
        print 'i:' + str(counted[i]) + ' probability_sum[i] -> ' + str(probability_sum[i]) 

    print probability_sum
    if(SHOW_POISSON_GRAPH):
        plt.figure(4)
        count, bins, ignored = plt.hist(probability, 14, density = True)
        plt.title("Poisson distribution for burst lenght, lamba = " + str(poisson_lambda)) 
        plt.xlabel("Burst Size (amount of lost fragments)") 
        plt.ylabel("Probability")
        plt.show()
    #print probability
final_burst = False
inline_bust =  False
enter_burst = False

while bitmap_size < bitmap_size_max:
    print "bitmap_size: " + str(bitmap_size)
    counter = 0

    output_array = []
    result_amount = {}
    np_output = []
    
    while counter < repetitions:
        #print "repetition: " + str(counter)
        counter2 = 0
        data = []
        counter3 = 0
        while counter2 < bitmap_size:
            final_burst = False
            inline_bust =  False
            enter_burst = False

            if BITMAP_GENERATION == 'TEST':
                counter2 = counter2 + 1
                data.append(1)
                burst_prob_apparence[1] += 1 
                print counter2

            if BITMAP_GENERATION == BURST:
                '''Generate bitmap using random poisson'''
                counter2 = counter2 + 1
                #print counter2
                if random.randint(0,1000) <= (1000 * FER):
                    output = 0
                    #burst_prob_apparence[0] += 1
                    #print 'ENTER BURST ' + str(counter2)
                    enter_burst = True
                    
                    burst_randomInt = random.randint(0,poisson_repetitions)
                    #print burst_randomInt
                    #burst_randomInt = 5
                    for burst_size in probability_sum:
                        if burst_randomInt <= probability_sum[burst_size]:
                            #print 'burst_size = ' + str(burst_size) + ' probabilitySum[i] ' + str(probability_sum[burst_size])
                            #Check if burst is larger than what is left of the bitmap
                            burst_start_position = counter2
                            burst_size_total_results[burst_size] += 1
                            #print burst_size_total_results
                            #print 'burst_start_position -> ' + str(burst_start_position) + ' bitmap_size -> ' + str(bitmap_size)
                            #print 'burst_start_position counter2 -> ' + str(counter2) + " len data -> " + str(len(data)) + ' end position -> ' + str(burst_start_position + burst_size)
                            if (burst_start_position + burst_size) <= bitmap_size:
                                inline_bust = True
                                #print data                            
                                #print 'filling the 0 NOT at the end burst_start_position -> '+ str(burst_start_position) +' burst_size -> ' + str(burst_size) + ' counter -> ' +str(counter2)
                                burst_size_real_total_results[burst_size] += 1
                                while counter2 <= burst_start_position + burst_size:
                                    #append the 0 of the bust
                                    #print ' counter -> ' +str(counter2) + ' data before -> ' + str(data)
                                    data.append(output)
                                    burst_prob_apparence[0] += 1   
                                    #print 'data after -> ' + str(data)   
                                    counter2 = counter2 + 1
                                    #print ' counter -> ' +str(counter2) + ' data after -> ' + str(data)

                                counter2 -= 1
                                #print 'burst counter2 -> ' + str(counter2) + " len data -> " + str(len(data))
                                break
                            else:
                                final_burst = True
                                burst_size_real_total_results[bitmap_size - counter2 + 1] += 1
                                #print data
                                #print 'filling the 0 at the END burst_start_position -> '+ str(burst_start_position) +' burst_size -> ' + str(burst_size)
                                #print 'burst real size -> ' + str(bitmap_size - counter2 + 1)
                                #print burst_size_total_results
                                while counter2 <= bitmap_size:
                                    #append the 0 of the bust
                                    #print ' counter -> ' +str(counter2) + ' data before -> ' + str(data)
                                   
                                    data.append(output)
                                    burst_prob_apparence[0] += 1      
                                    counter2 = counter2 + 1
                                    #print ' counter -> ' +str(counter2) + ' data after -> ' + str(data)

                                #print data
                                counter2 -= 1
                                #print 'burst END counter2 -> ' + str(counter2) + "len data -> " + str(len(data))
                                break
                            print 'never'
                    #zeros = zeros + 1
                else:
                    output = 1
                    data.append(output)
                    burst_prob_apparence[1] += 1        
                    #ones = ones + 1

            elif BITMAP_GENERATION == RANDOM:
                '''Generate bitmap using random'''
                counter2 = counter2 + 1
                if random.randint(0,1000) <= FER_RANDOM * 10:
                    output = 0
                    burst_prob_apparence[0] += 1 
                    #zeros = zeros + 1
                else:
                    output = 1
                    burst_prob_apparence[1] += 1 
                    #ones = ones + 1
                data.append(output)
            
            
            if len(data)!= counter2:
                print 'data len-> '+str(len(data)) + ' counter2-> '+str(counter2)
                print 'data -> ' + str(data) 
                print 'inline_bust ->'+ str(inline_bust)+' final_burst -> ' + str(final_burst) + ' enter_burst -> ' + str(enter_burst)
                print 'NOT equal'
                print 'burst_size = ' + str(burst_size) + ' probabilitySum[i] ' + str(probability_sum[burst_size])
                print burst_randomInt
                print "burst_start_position + burst_size -> " +str(burst_start_position) + str(burst_size) 
                raw_input()
            #raw_input('continue.....')
        #print str(data) + " size -> " + str(len(data))
        #print 'END - counter2 -> ' + str(counter2) + " len data -> " + str(len(data))
        #print 'append data'
        #print data
        np_output.append(np.array(data))
        #print 'data lenght -> ' + str(len(data)) + ' data -> ' + str(data)
        if len(data) == bitmap_size:
            output_array.append(data)
        else:
            print 'ERROR IN LENGHT'
            print 'lenght -> ' + str(len(data))
            print 'END - counter2 -> ' + str(counter2) + " len data -> " + str(len(data))
            print data
            print 'bitmap_size = ' + str(bitmap_size)
            print 'bitmap_size_max = ' + str(bitmap_size_max)
            print 'bitmap_delta = ' + str(bitmap_delta)
            #print output_array
            raw_input('')
            break
        #print np_output
        #raw_input('')


        #s = pd.DataFrame(data, index = 0, columns = index)
        #print s     
        counter = counter + 1
    #print len(np_output)
    #print np_output
    if(SHOW_BITMAP_IMAGE):
        np_output_array = np.array(np_output)
        #print np_output_array
        #print np_output_array.shape
        np_output_reshape = np_output_array.reshape(repetitions, bitmap_size)
        plt.figure(10)
        plt.imshow(np_output_reshape, cmap="gray")
        plt.title("Repetitions vs bitmap size " + (BITMAP_GENERATION) + ' Fragments: ' + str(bitmap_size) ) 
        plt.xlabel("bitmap size (fragments)") 
        plt.ylabel("Repetition") 
        plt.show()
    #im = Image.fromarray(255*np_output_array,'L')
    #print im
    #im.show()

    print "prob of 0 -> " + str((burst_prob_apparence[0]/(burst_prob_apparence[0]+burst_prob_apparence[1])*100)) + '%'   
    

    if (burst_prob_apparence[0]/(burst_prob_apparence[0]+burst_prob_apparence[1])*100) != 0:
        probability_total_summary[bitmap_size] = (burst_prob_apparence[0]/(burst_prob_apparence[0]+burst_prob_apparence[1])*100)
    else:
        probability_total_summary[bitmap_size] = 0
    burst_size_total_summary[bitmap_size] = burst_size_total_results
    burst_size_real_total_summary[bitmap_size] = burst_size_real_total_results
    if PRINT_ALL:
        print "burst_prob_apparence -> " + str(burst_prob_apparence)
        print "burst_size_total_summary -> " + str(burst_size_total_summary)
        print "burst_size_real_total_summary -> " + str(burst_size_real_total_summary)
        print probability_total_summary
    '''Burst test uncomment for burst graphs'''
    if SHOW_BURST_GRAPH:
        plt.figure(33)
        lists = sorted(burst_size_total_results.items()) # sorted by key, return a list of tuples

        x, y = zip(*lists) # unpack a list of pairs into two tuples
        plt.bar(x, y)
        plt.xticks(x,x)
        plt.title("Burst size apperance") 
        plt.xlabel("burst size") 
        plt.ylabel("number of appearence")
        print 'burst_size_total_results ->'+ str(burst_size_total_results)
        
        for i in burst_size_total_results:
            print str(i)+','+ str(burst_size_total_results[i])


        plt.figure(34)
        lists = sorted(burst_size_real_total_results.items()) # sorted by key, return a list of tuples

        x, y = zip(*lists) # unpack a list of pairs into two tuples
        plt.bar(x, y)
        plt.xticks(x,x)
        plt.title("Burst real size apperance") 
        plt.xlabel("burst size") 
        plt.ylabel("number of appearence")
        print 'burst_size_real_total_results ->' + str(burst_size_real_total_results)
        for i in burst_size_real_total_results:
            print str(i)+','+ str(burst_size_real_total_results[i])

        print 'burst_prob_apparence' + str(burst_prob_apparence)
        plt.show()    
    
    '''
    a = np.array(output_array)
    print a
    #unique, counts = np.unique(a, return_counts=True)
    prob_cal = dict()
    total_ones = 0
    total_zeros = 0
    total_prob = defaultdict(float)
    for bitmap in output_array:
        #print bitmap
        a = np.array(bitmap)
        
        #print dict(zip(*np.unique(a, return_counts=True)))
        prob_cal =  dict(zip(*np.unique(a, return_counts=True)))
        for i in prob_cal:
            total_prob[i] += prob_cal[i] 
            #print prob_cal[i]
            #print total_prob

    print total_prob
    #total = 0.0
    probability_total_summary_provisional = defaultdict(float)
    for value in total_prob:
    #    print value 
    #    print prob_cal[value]
    #    total = total + prob_cal[value]
    #    print total
        print str(value)+'-> '+str(100*(total_prob[value]/(repetitions*bitmap_size))) + '%'

        probability_total_summary_provisional[value] = 100*(total_prob[value]/(repetitions*bitmap_size))
    if probability_total_summary_provisional[0]:

        probability_total_summary[bitmap_size] = probability_total_summary_provisional[0]
    else:
        probability_total_summary[bitmap_size] = 0
    '''
    
    
    '''
    columns = (a != 0).sum(0)
    rows    = (a != 0).sum(1)
    print columns
    print rows
    porcentaje_array = []
    index_array = []
    for value in range(len(columns)):
        print "bit:"+ str(value+1) +" Porcentaje of zeros: "+str(100*(1-columns[value]/repetitions))
        porcentaje_array.append(100*(1-columns[value]/repetitions))
        index_array.append(value+1)

    plt.figure(1)
    plt.title("Porcentaje of zeros per bit") 
    plt.xlabel("bit number") 
    plt.ylabel("porcentaje") 
    plt.plot(index_array,porcentaje_array) 
    plt.xticks(index_array, index_array)

    plt.show()
    '''
    #raw_input('')
    
    #bitmap_size = bitmap_size + 1

    ''' bitmap calculations'''
    bitmap_res = defaultdict(float)
    zero_found = False
    for bitmap in range(len(output_array)):
        #print "bitmap length -> " + str(len(output_array[bitmap]))
        for bit in output_array[bitmap]:
            #print "bit -> " + str(bit)
            if not bit:
                #print "bit equal 0"
                #bit equal 0, bitmap of max size
                bitmap_res[len(output_array[bitmap])] += 1
                zero_found = True
                break
        #no 0 found in bitmap, size of bitmap = 0
        if not zero_found:
            bitmap_res[0] += 1
        zero_found = False

    print "bitmap_res -> " +str(bitmap_res)

    BitmapResults = defaultdict(float)

    BitmapResults = bit_to_bytes(bitmap_res)

    if PRINT_ALL:
        print BitmapResults
        print 'BitmapResults'    
    #print BitmapResults
    #raw_input('BitmapResults')
    '''FRAME CALCULATION FOR BITMAP'''

    bitmap_results_frames_lora[bitmap_size] = frames_calculation(LORA_PAYLOAD,BitmapResults)
    bitmap_results_frames_lora_pdf[bitmap_size] = pdf_calculation(bitmap_results_frames_lora[bitmap_size], repetitions)
    bitmap_results_frames_lora_prob[bitmap_size] = average_calculation(bitmap_results_frames_lora_pdf[bitmap_size])
    bitmap_results_frames_lora_variance[bitmap_size] = variance_calculation(bitmap_results_frames_lora[bitmap_size])
    bitmap_results_frames_lora_sd[bitmap_size] = sd_calculation(bitmap_results_frames_lora[bitmap_size])

    ''' variance and standard deviation calculation '''
    sum_of_numbers = sum(number*count for number, count in bitmap_results_frames_lora[bitmap_size].iteritems())
    count = sum(count for n, count in bitmap_results_frames_lora[bitmap_size].iteritems())
    mean = sum_of_numbers / count
    # print mean
    total_squares = sum(number*number * count for number, count in bitmap_results_frames_lora[bitmap_size].iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    # print variance
    # print std_dev
    bitmap_results_frames_lora_variance[bitmap_size] = variance
    bitmap_results_frames_lora_sd[bitmap_size] = std_dev

    # print bitmap_results_frames_lora_variance
    # print bitmap_results_frames_lora_sd

    '''TOA CALCULATION'''
    bitmap_results_TOA[bitmap_size] = TOA_dic_calculation(BitmapResults)
    print "bitmap_results_TOA[bitmap_size]-> " + str(bitmap_results_TOA[bitmap_size])
    bitmap_results_TOA_variance[bitmap_size] = TOA_dic_calculation_variance(BitmapResults)
    bitmap_results_TOA_sd[bitmap_size] = TOA_dic_calculation_sd(BitmapResults)

    if PRINT_ALL:
        print bitmap_results_frames_lora
        print bitmap_results_frames_lora_pdf
        print bitmap_results_frames_lora_prob
        print bitmap_results_TOA
        print bitmap_results_TOA_variance
        print bitmap_results_TOA_sd


    #raw_input(".....")
    '''Optimized bitmap calculation'''
    optimizedBitmap = defaultdict(float)
    #print optimizedBitmap
    #Found first zero from right to left
    for bitmap in range(len(output_array)):
        #print str(output_array[bitmap])
        counter = 0
        for bit in reversed(output_array[bitmap]):
            
            if bit:
                #print "1 found"
                pass
            else:
                #print "0 found - " + "pos: " + str(bitmap_size - counter)
                #if (bitmap_size - counter) in optimizedBitmap:
                optimizedBitmap[bitmap_size - counter] += 1
                #    
                #else:
                #    optimizedBitmap[bitmap_size - counter] = 1
                break
            counter = counter + 1
            if counter == bitmap_size:
                optimizedBitmap[bitmap_size - counter] += 1
    if PRINT_ALL:
        print "optimizedBitmap"
        print optimizedBitmap


    optimizedBitmapResults = defaultdict(float)
   
    optimizedBitmapResults = bit_to_bytes(optimizedBitmap)
    if PRINT_ALL:
        print optimizedBitmapResults
        print 'optimizedBitmapResults'    
    #print optimizedBitmapResults
    #raw_input('optimizedBitmapResults')



    '''FRAME CALCULATION FOR COMPRESSED BITMAP'''

    compressed_bitmap_results_frames_lora[bitmap_size] = frames_calculation(LORA_PAYLOAD,optimizedBitmapResults)
    compressed_bitmap_results_frames_lora_pdf[bitmap_size] = pdf_calculation(compressed_bitmap_results_frames_lora[bitmap_size], repetitions)
    compressed_bitmap_results_frames_lora_prob[bitmap_size] = average_calculation(compressed_bitmap_results_frames_lora_pdf[bitmap_size])
    compressed_bitmap_results_frames_lora_variance[bitmap_size] = variance_calculation(compressed_bitmap_results_frames_lora[bitmap_size])
    compressed_bitmap_results_frames_lora_sd[bitmap_size] = sd_calculation(compressed_bitmap_results_frames_lora[bitmap_size])


    '''TOA CALCULATION'''
    compressed_bitmap_results_TOA[bitmap_size] = TOA_dic_calculation(optimizedBitmapResults)
    compressed_bitmap_results_TOA_variance[bitmap_size] = TOA_dic_calculation_variance(optimizedBitmapResults)
    compressed_bitmap_results_TOA_sd[bitmap_size] = TOA_dic_calculation_sd(optimizedBitmapResults)


    if PRINT_ALL:
        print compressed_bitmap_results_frames_lora
        print compressed_bitmap_results_frames_lora_pdf
        print compressed_bitmap_results_frames_lora_prob
        print compressed_bitmap_results_TOA
   

    #list of deltas calculation
    #list_of_deltas = defaultdict(float)
    #deltas_bit_size = defaultdict(float)
    list_of_deltas_real_results_bits = defaultdict(float)
    #print "list_of_deltas -> " + str(list_of_deltas)
    
    list_of_deltas_sdnv_2 = defaultdict(float)
    list_of_deltas_sdnv_3 = defaultdict(float)
    list_of_deltas_sdnv_4 = defaultdict(float)
    list_of_deltas_sdnv_5 = defaultdict(float)
    deltas_bit_size_sdnv_2 = defaultdict(float)
    deltas_bit_size_sdnv_3 = defaultdict(float)
    deltas_bit_size_sdnv_4 = defaultdict(float)
    deltas_bit_size_sdnv_5 = defaultdict(float)
    '''real is for all'''
    list_of_deltas_real_results_bits_sdnv_2 = defaultdict(float)
    list_of_deltas_real_results_bits_sdnv_3 = defaultdict(float)
    list_of_deltas_real_results_bits_sdnv_4 = defaultdict(float)
    list_of_deltas_real_results_bits_sdnv_5 = defaultdict(float)
    

    #Found first zero from right to left
    for bitmap in range(len(output_array)):
        lastpos = 0
        sdnv_value = 0
        difference = 0
        #ack_resp_size = 0 #response size in bits
        ack_resp_size_sdnv_2 = 0 #response size in bits
        ack_resp_size_sdnv_3 = 0 #response size in bits
        ack_resp_size_sdnv_4 = 0 #response size in bits
        ack_resp_size_sdnv_5 = 0 #response size in bits
        
        #print str(output_array[bitmap]) 0
        position = 1
        for bit in output_array[bitmap]:
            
            if bit:
                #print "1 found"
                pass
            else:
                #print "0 found - " + "pos: " + str(position)
                if lastpos != 0:
                    difference = position - lastpos
                    #print 'lastpos -> '+str(lastpos)+' difference -> ' + str(difference) 
                    list_of_deltas_real_results_bits[difference] += 1
                    lastpos = position
                    
                    #if DELTA_BASE_SIZE == 2:
                    if difference <= 1:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 2
                        deltas_bit_size_sdnv_2[2] += 1
                    elif difference <= 3:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 4
                        deltas_bit_size_sdnv_2[4] += 1
                    elif difference <= 7:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 6
                        deltas_bit_size_sdnv_2[6] += 1
                    elif difference <= 15:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 8
                        deltas_bit_size_sdnv_2[8] += 1
                    elif difference <= 31:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 10
                        deltas_bit_size_sdnv_2[10] += 1
                    elif difference <= 63:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 12
                        deltas_bit_size_sdnv_2[12] += 1
                    elif difference <= 127:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 14
                        deltas_bit_size_sdnv_2[14] += 1


                    #elif DELTA_BASE_SIZE == 3:
                    if difference <= 3:
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 3
                        deltas_bit_size_sdnv_3[3] += 1
                    elif difference <= 15:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 6
                        deltas_bit_size_sdnv_3[6] += 1

                    elif difference <= 63:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 9
                        #ack_resp_size_sdnv_3 += 9
                        deltas_bit_size_sdnv_3[9] += 1
                    elif difference <= 255:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 12
                        deltas_bit_size_sdnv_3[12] += 1
                    
                    #elif DELTA_BASE_SIZE == 4:
                    if difference <= 7:
                        #print 'difference < 7 add 4 bits'
                        ack_resp_size_sdnv_4 = ack_resp_size_sdnv_4 + 4
                        deltas_bit_size_sdnv_4[4] += 1
                    elif difference <= 63:
                        #print 'difference < 63 add 8 bits'
                        ack_resp_size_sdnv_4 = ack_resp_size_sdnv_4 + 8
                        deltas_bit_size_sdnv_4[8] += 1
                    elif difference <= 511:
                        #print 'difference < 511 add 12 bits'
                        ack_resp_size_sdnv_4 = ack_resp_size_sdnv_4 + 12
                        deltas_bit_size_sdnv_4[12] += 1
                    #print 'current ack size -> ' + str(ack_resp_size)

                    #elif DELTA_BASE_SIZE == 5:
                    #    ''' X0000 -> 4 bits useful diff -> 15'''
                        
                    if difference <= 15:
                        ack_resp_size_sdnv_5 = ack_resp_size_sdnv_5 + 5
                        deltas_bit_size_sdnv_5[5] += 1
                    elif difference <= 255:
                        ack_resp_size_sdnv_5 = ack_resp_size_sdnv_5 + 10
                        deltas_bit_size_sdnv_5[10] += 1
                    
                    #elif DELTA_BASE_SIZE == 6:
                        ''' X00000 -> 5 bits useful diff -> 31'''
                    #    if difference <= 31:
                    #        ack_resp_size_sdnv_5 = ack_resp_size_sdnv_5 + 6
                    #        deltas_bit_size[6] += 1
                    #    elif difference <= 1023:
                    #        ack_resp_size = ack_resp_size + 12
                    #        deltas_bit_size[12] += 1
                else:
                    lastpos = position
                    #print 'lastpos -> '+str(lastpos)
                    list_of_deltas_real_results_bits[lastpos] += 1

                    #if DELTA_BASE_SIZE == 2:
                    if lastpos <= 1:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 2
                        deltas_bit_size_sdnv_2[2] += 1
                    elif lastpos <= 3:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 4
                        deltas_bit_size_sdnv_2[4] += 1
                    elif lastpos <= 7:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 6
                        deltas_bit_size_sdnv_2[6] += 1
                    elif lastpos <= 15:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 8
                        deltas_bit_size_sdnv_2[8] += 1
                    elif lastpos <= 31:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 10
                        deltas_bit_size_sdnv_2[10] += 1
                    elif lastpos <= 63:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 12
                        deltas_bit_size_sdnv_2[12] += 1
                    elif lastpos <= 127:
                        ack_resp_size_sdnv_2 = ack_resp_size_sdnv_2 + 14
                        deltas_bit_size_sdnv_2[14] += 1
                    
                    #elif DELTA_BASE_SIZE == 3:
                    if lastpos <= 3:
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 3
                        deltas_bit_size_sdnv_3[3] += 1
                    elif lastpos <= 15:
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 6
                        deltas_bit_size_sdnv_3[6] += 1
                    elif lastpos <= 63:
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 9
                        deltas_bit_size_sdnv_3[9] += 1
                    elif lastpos <= 255:
                        ack_resp_size_sdnv_3 = ack_resp_size_sdnv_3 + 12
                        deltas_bit_size_sdnv_3[12] += 1
                
                    #elif DELTA_BASE_SIZE == 4:
                    if lastpos <= 7:
                        ack_resp_size_sdnv_4 = ack_resp_size_sdnv_4 + 4
                        deltas_bit_size_sdnv_4[4] += 1
                    elif lastpos <= 63:
                        ack_resp_size_sdnv_4 = ack_resp_size_sdnv_4 + 8
                        deltas_bit_size_sdnv_4[8] += 1
                    elif lastpos <= 511:
                        ack_resp_size_sdnv_4 = ack_resp_size_sdnv_4 + 12
                        deltas_bit_size_sdnv_4[12] += 1
                    #elif DELTA_BASE_SIZE == 5:
                    if lastpos <= 15:
                        ack_resp_size_sdnv_5 = ack_resp_size_sdnv_5 + 5
                        deltas_bit_size_sdnv_5[5] += 1
                    elif lastpos <= 255:
                        ack_resp_size_sdnv_5 = ack_resp_size_sdnv_5 + 10
                        deltas_bit_size_sdnv_5[10] += 1

                    #elif DELTA_BASE_SIZE == 6:
                    #    ''' X00000 -> 5 bits useful diff -> 31'''
                    #    if lastpos <= 31:
                    #        ack_resp_size = ack_resp_size + 6
                    #        deltas_bit_size[6] += 1
                    #    elif lastpos <= 1023:
                    #        ack_resp_size = ack_resp_size + 12
                    #        deltas_bit_size[12] += 1
                        #print 'lastpos < 511 add 12 bits'
                    #print 'current ack size -> ' + str(ack_resp_size)


               
            position = position + 1

        #print "ack_resp_size_sdnv_5 -> " + str(ack_resp_size_sdnv_5) + ' list_of_deltas_sdnv_5[ack_resp_size_sdnv_5] -> ' + str(list_of_deltas_sdnv_5[ack_resp_size_sdnv_5])
        #print "ack_resp_size_sdnv_4 -> " + str(ack_resp_size_sdnv_4) + ' list_of_deltas_sdnv_4[ack_resp_size_sdnv_4] -> ' + str(list_of_deltas_sdnv_5[ack_resp_size_sdnv_4])
        
        #list_of_deltas[ack_resp_size] += 1
        list_of_deltas_sdnv_2[ack_resp_size_sdnv_2] += 1
        list_of_deltas_sdnv_3[ack_resp_size_sdnv_3] += 1
        list_of_deltas_sdnv_4[ack_resp_size_sdnv_4] += 1
        list_of_deltas_sdnv_5[ack_resp_size_sdnv_5] += 1
        


    #print "list_of_deltas -> " + str(list_of_deltas)
    if PRINT_ALL:
        print 'list_of_deltas 2 '+ str(list_of_deltas_sdnv_2)
        print 'list_of_deltas 3 '+ str(list_of_deltas_sdnv_3)
        print 'list_of_deltas 4 '+ str(list_of_deltas_sdnv_4)
        print 'list_of_deltas 5 '+ str(list_of_deltas_sdnv_5)

    #list_of_deltas_results_bits[bitmap_size] = deltas_bit_size
    #print "list_of_deltas_results_bits -> " + str(list_of_deltas_results_bits)
    
    list_of_deltas_results_bits_sdnv_2[bitmap_size] = deltas_bit_size_sdnv_2
    
    list_of_deltas_results_bits_sdnv_3[bitmap_size] = deltas_bit_size_sdnv_3
    
    list_of_deltas_results_bits_sdnv_4[bitmap_size] = deltas_bit_size_sdnv_4
    
    list_of_deltas_results_bits_sdnv_5[bitmap_size] = deltas_bit_size_sdnv_5
    if PRINT_ALL:
        print "list_of_deltas_results_bits_sdnv_2 -> " + str(list_of_deltas_results_bits_sdnv_2)
        print "list_of_deltas_results_bits_sdnv_3 -> " + str(list_of_deltas_results_bits_sdnv_3)
        print "list_of_deltas_results_bits_sdnv_4 -> " + str(list_of_deltas_results_bits_sdnv_4)
        print "list_of_deltas_results_bits_sdnv_5 -> " + str(list_of_deltas_results_bits_sdnv_5)
    
    
    '''Convertion from bits to bytes'''
    #list_of_deltas_results_bytes_provisional = defaultdict(float)
    list_of_deltas_results_bytes_provisional_sdnv_2 = defaultdict(float)
    list_of_deltas_results_bytes_provisional_sdnv_3 = defaultdict(float)
    list_of_deltas_results_bytes_provisional_sdnv_4 = defaultdict(float)
    list_of_deltas_results_bytes_provisional_sdnv_5 = defaultdict(float)


    #LoD-2 SDNV-2
    list_of_deltas_results_bytes_provisional_sdnv_2 = bit_to_bytes(list_of_deltas_sdnv_2)
    list_of_deltas_results_bytes_sdnv_2[bitmap_size] = list_of_deltas_results_bytes_provisional_sdnv_2
    if PRINT_ALL:
        print 'list_of_deltas_results_bytes_sdnv_2 -> ' + str(list_of_deltas_results_bytes_sdnv_2)

    '''Frames calculation LoD-2 (SDNV-2)'''
    list_of_deltas_sdnv_2_results_frames_lora[bitmap_size] =  frames_calculation(LORA_PAYLOAD, list_of_deltas_results_bytes_provisional_sdnv_2)
    list_of_deltas_sdnv_2_results_frames_lora_pdf[bitmap_size] = pdf_calculation(list_of_deltas_sdnv_2_results_frames_lora[bitmap_size], repetitions)
    list_of_deltas_sdnv_2_results_frames_lora_prob[bitmap_size] = average_calculation(list_of_deltas_sdnv_2_results_frames_lora_pdf[bitmap_size])
    list_of_deltas_sdnv_2_results_frames_lora_variance[bitmap_size] = variance_calculation(list_of_deltas_sdnv_2_results_frames_lora[bitmap_size])
    list_of_deltas_sdnv_2_results_frames_lora_sd[bitmap_size] = sd_calculation(list_of_deltas_sdnv_2_results_frames_lora[bitmap_size])
    '''TOA CALCULATION'''
    list_of_deltas_sdnv_2_results_TOA[bitmap_size] = TOA_dic_calculation(list_of_deltas_results_bytes_provisional_sdnv_2)
    list_of_deltas_sdnv_2_results_TOA_variance[bitmap_size] = TOA_dic_calculation_variance(list_of_deltas_results_bytes_provisional_sdnv_2)
    list_of_deltas_sdnv_2_results_TOA_sd[bitmap_size] = TOA_dic_calculation_sd(list_of_deltas_results_bytes_provisional_sdnv_2)


    if PRINT_ALL:
        print list_of_deltas_sdnv_2_results_frames_lora
        print list_of_deltas_sdnv_2_results_frames_lora_pdf
        print list_of_deltas_sdnv_2_results_frames_lora_prob
        print list_of_deltas_sdnv_2_results_TOA
    #LoD-3 SDNV_3
    '''Frames calculation LoD-3 (SDNV-3)'''    
    list_of_deltas_results_bytes_provisional_sdnv_3 = bit_to_bytes(list_of_deltas_sdnv_3)
    list_of_deltas_results_bytes_sdnv_3[bitmap_size] = list_of_deltas_results_bytes_provisional_sdnv_3
    list_of_deltas_sdnv_3_results_frames_lora[bitmap_size] =  frames_calculation(LORA_PAYLOAD, list_of_deltas_results_bytes_provisional_sdnv_3)
    list_of_deltas_sdnv_3_results_frames_lora_pdf[bitmap_size] = pdf_calculation(list_of_deltas_sdnv_3_results_frames_lora[bitmap_size], repetitions)
    list_of_deltas_sdnv_3_results_frames_lora_prob[bitmap_size] = average_calculation(list_of_deltas_sdnv_3_results_frames_lora_pdf[bitmap_size])
    list_of_deltas_sdnv_3_results_frames_lora_variance[bitmap_size] = variance_calculation(list_of_deltas_sdnv_3_results_frames_lora[bitmap_size])
    list_of_deltas_sdnv_3_results_frames_lora_sd[bitmap_size] = sd_calculation(list_of_deltas_sdnv_3_results_frames_lora[bitmap_size])
    '''TOA CALCULATION'''
 
    list_of_deltas_sdnv_3_results_TOA[bitmap_size] = TOA_dic_calculation(list_of_deltas_results_bytes_provisional_sdnv_3)
    list_of_deltas_sdnv_3_results_TOA_variance[bitmap_size] = TOA_dic_calculation_variance(list_of_deltas_results_bytes_provisional_sdnv_3)
    list_of_deltas_sdnv_3_results_TOA_sd[bitmap_size] = TOA_dic_calculation_sd(list_of_deltas_results_bytes_provisional_sdnv_3)

    if PRINT_ALL:
        print 'list_of_deltas_results_bytes_sdnv_3 -> ' + str(list_of_deltas_results_bytes_sdnv_3)
        print list_of_deltas_sdnv_3_results_frames_lora
        print list_of_deltas_sdnv_3_results_frames_lora_pdf
        print list_of_deltas_sdnv_3_results_frames_lora_prob
        print list_of_deltas_sdnv_3_results_TOA

    #LoD-4 SDNV_4
    '''Frames calculation LoD-4 (SDNV-4)'''    

    list_of_deltas_results_bytes_provisional_sdnv_4 = bit_to_bytes(list_of_deltas_sdnv_4)
    list_of_deltas_results_bytes_sdnv_4[bitmap_size] = list_of_deltas_results_bytes_provisional_sdnv_4


    list_of_deltas_sdnv_4_results_frames_lora[bitmap_size] =  frames_calculation(LORA_PAYLOAD, list_of_deltas_results_bytes_provisional_sdnv_4)
    list_of_deltas_sdnv_4_results_frames_lora_pdf[bitmap_size] = pdf_calculation(list_of_deltas_sdnv_4_results_frames_lora[bitmap_size], repetitions)
    list_of_deltas_sdnv_4_results_frames_lora_prob[bitmap_size] = average_calculation(list_of_deltas_sdnv_4_results_frames_lora_pdf[bitmap_size])
    list_of_deltas_sdnv_4_results_frames_lora_variance[bitmap_size] = variance_calculation(list_of_deltas_sdnv_4_results_frames_lora[bitmap_size])
    list_of_deltas_sdnv_4_results_frames_lora_sd[bitmap_size] = sd_calculation(list_of_deltas_sdnv_4_results_frames_lora[bitmap_size])
    '''TOA CALCULATION'''
    list_of_deltas_sdnv_4_results_TOA[bitmap_size] = TOA_dic_calculation(list_of_deltas_results_bytes_provisional_sdnv_4)
    list_of_deltas_sdnv_4_results_TOA_variance[bitmap_size] = TOA_dic_calculation_variance(list_of_deltas_results_bytes_provisional_sdnv_4)
    list_of_deltas_sdnv_4_results_TOA_sd[bitmap_size] = TOA_dic_calculation_sd(list_of_deltas_results_bytes_provisional_sdnv_4)

    if PRINT_ALL:
        print 'list_of_deltas_results_bytes_sdnv_4 -> ' + str(list_of_deltas_results_bytes_sdnv_4)
        print list_of_deltas_sdnv_4_results_frames_lora
        print list_of_deltas_sdnv_4_results_frames_lora_pdf
        print list_of_deltas_sdnv_4_results_frames_lora_prob
        print list_of_deltas_sdnv_4_results_TOA

    #LoD-5 SDNV_5
    '''Frames calculation LoD-5 (SDNV-5)'''      
    list_of_deltas_results_bytes_provisional_sdnv_5 = bit_to_bytes(list_of_deltas_sdnv_5)
    list_of_deltas_results_bytes_sdnv_5[bitmap_size] = list_of_deltas_results_bytes_provisional_sdnv_5


    list_of_deltas_sdnv_5_results_frames_lora[bitmap_size] =  frames_calculation(LORA_PAYLOAD, list_of_deltas_results_bytes_provisional_sdnv_5)
    list_of_deltas_sdnv_5_results_frames_lora_pdf[bitmap_size] = pdf_calculation(list_of_deltas_sdnv_5_results_frames_lora[bitmap_size], repetitions)
    list_of_deltas_sdnv_5_results_frames_lora_prob[bitmap_size] = average_calculation(list_of_deltas_sdnv_5_results_frames_lora_pdf[bitmap_size])
    list_of_deltas_sdnv_5_results_frames_lora_variance[bitmap_size] = variance_calculation(list_of_deltas_sdnv_5_results_frames_lora[bitmap_size])
    list_of_deltas_sdnv_5_results_frames_lora_sd[bitmap_size] = sd_calculation(list_of_deltas_sdnv_5_results_frames_lora[bitmap_size])
    '''TOA CALCULATION'''
    list_of_deltas_sdnv_5_results_TOA[bitmap_size] = TOA_dic_calculation(list_of_deltas_results_bytes_provisional_sdnv_5)
    list_of_deltas_sdnv_5_results_TOA_variance[bitmap_size] = TOA_dic_calculation_variance(list_of_deltas_results_bytes_provisional_sdnv_5)
    list_of_deltas_sdnv_5_results_TOA_sd[bitmap_size] = TOA_dic_calculation_sd(list_of_deltas_results_bytes_provisional_sdnv_5)

    if PRINT_ALL:
        print 'list_of_deltas_results_bytes_sdnv_5 -> ' + str(list_of_deltas_results_bytes_sdnv_5)
        print list_of_deltas_sdnv_5_results_frames_lora
        print list_of_deltas_sdnv_5_results_frames_lora_pdf
        print list_of_deltas_sdnv_5_results_frames_lora_prob
        print list_of_deltas_sdnv_5_results_TOA


    #list of fragment #
    list_of_fragments_numbers = defaultdict(float)
    #print "list_of_fragments_numbers -> " + str(list_of_fragments_numbers)

    #Found first zero from right to left
    for bitmap in range(len(output_array)):
        lastpos = 0
        ack_resp_size = 0 #response size in bits
        #print str(output_array[bitmap])
        position = 1
        for bit in output_array[bitmap]:
            
            if bit:
                #print "1 found"
                pass
            else:
                #print "0 found - " + "pos: " + str(position)
                ack_resp_size = ack_resp_size + list_of_fragments_numbers_lenght
                #print 'current ack size -> ' + str(ack_resp_size)       
                
            position = position + 1

        #print "ack_resp_size -> " + str(ack_resp_size)
        list_of_fragments_numbers[ack_resp_size] += 1

    list_of_fragments_numbers_result_bits[bitmap_size] = list_of_fragments_numbers
    if PRINT_ALL:
        print "list_of_fragments_numbers -> " + str((list_of_fragments_numbers))
        print "list_of_fragments_numbers_result_bits -> " + str((list_of_fragments_numbers_result_bits))

    '''Convertion from bits to bytes'''
    list_of_fragments_numbers_result_bytes_provisional = defaultdict(float)
    
    list_of_fragments_numbers_result_bytes_provisional = bit_to_bytes(list_of_fragments_numbers)
    list_of_fragments_numbers_result_bytes[bitmap_size] = list_of_fragments_numbers_result_bytes_provisional
    #LLF 
    '''Frames calculation LLF'''      
    list_of_fragments_numbers_results_frames_lora[bitmap_size] =  frames_calculation(LORA_PAYLOAD, list_of_fragments_numbers_result_bytes_provisional)
    list_of_fragments_numbers_results_frames_lora_pdf[bitmap_size] = pdf_calculation(list_of_fragments_numbers_results_frames_lora[bitmap_size], repetitions)
    list_of_fragments_numbers_results_frames_lora_prob[bitmap_size] = average_calculation(list_of_fragments_numbers_results_frames_lora_pdf[bitmap_size])
    list_of_fragments_numbers_results_frames_lora_variance[bitmap_size] = variance_calculation(list_of_fragments_numbers_results_frames_lora[bitmap_size])
    list_of_fragments_numbers_results_frames_lora_sd[bitmap_size] = sd_calculation(list_of_fragments_numbers_results_frames_lora[bitmap_size])
    '''TOA CALCULATION'''
    list_of_fragments_numbers_results_TOA[bitmap_size] = TOA_dic_calculation(list_of_fragments_numbers_result_bytes_provisional)
    list_of_fragments_numbers_results_TOA_variance[bitmap_size] = TOA_dic_calculation_variance(list_of_fragments_numbers_result_bytes_provisional)
    list_of_fragments_numbers_results_TOA_sd[bitmap_size] = TOA_dic_calculation_sd(list_of_fragments_numbers_result_bytes_provisional)

    
    #raw_input('')
    if PRINT_ALL:
        print 'list_of_fragments_numbers_result_bytes-> '+str(list_of_fragments_numbers_result_bytes)
        print list_of_fragments_numbers_results_frames_lora
        print list_of_fragments_numbers_results_frames_lora_pdf
        print list_of_fragments_numbers_results_frames_lora_prob
        print list_of_fragments_numbers_results_TOA
    
   


    #bitmap#
    ''' variance and standard deviation calculation '''
    sum_of_numbers = sum(number*count for number, count in BitmapResults.iteritems())
    count = sum(count for n, count in BitmapResults.iteritems())
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in BitmapResults.iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    
    Bitmap_summary_variance[bitmap_size] = variance
    Bitmap_summary_sd[bitmap_size] = std_dev
    Bitmap_summary[bitmap_size] = mean

    if PRINT_ALL:
        print '\ninformation about the bitmap'
        print "Amount of bytes: amount of times " 
        print str(BitmapResults)
    # average = 0
    # provisional = 0
    # provisional2 = 0
    # for i in BitmapResults:
    #     provisional = provisional + BitmapResults[i] * i
    #     provisional2 = provisional2 + BitmapResults[i]
    #     #print "provisional: " + str(provisional)
    #     #print "provisionsal2: " + str(provisional2)
    # average = provisional / provisional2
    # Bitmap_summary[bitmap_size] = average
    if PRINT_ALL:
        print Bitmap_summary[bitmap_size]
    #print average_calculation(optimizedBitmapResults)
    #raw_input('')

    for i in BitmapResults:
        BitmapResults[i] = (BitmapResults[i]/repetitions)
    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples

    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    if PRINT_ALL:
    
        print "Amount of bytes: percentage of apperance " 
        print BitmapResults
    Bitmap_summary_bytes_probability[bitmap_size] = BitmapResults
    if PRINT_ALL:
    
        print "bitmap_size:average ack size in bytes" 
        print str(Bitmap_summary)
    #OptimizedBitmap
    ''' variance and standard deviation calculation '''
    sum_of_numbers = sum(number*count for number, count in optimizedBitmapResults.iteritems())
    count = sum(count for n, count in optimizedBitmap.iteritems())
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in optimizedBitmapResults.iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    
    optimizedBitmap_summary_variance[bitmap_size] = variance
    optimizedBitmap_summary_sd[bitmap_size] = std_dev
    optimizedBitmap_summary[bitmap_size] = mean
    if PRINT_ALL:
        print '\ninformation about the optimized bitmap'
        print "Amount of bytes: amount of times " 
        print str(optimizedBitmapResults)
    # average = 0
    # provisional = 0
    # provisional2 = 0
    # for i in optimizedBitmapResults:
    #     provisional = provisional + optimizedBitmapResults[i] * i
    #     provisional2 = provisional2 + optimizedBitmapResults[i]
    #     #print "provisional: " + str(provisional)
    #     #print "provisionsal2: " + str(provisional2)
    # average = provisional / provisional2
    # optimizedBitmap_summary[bitmap_size] = average
    if PRINT_ALL:
        print optimizedBitmap_summary[bitmap_size]
    #print average_calculation(optimizedBitmapResults)

    for i in optimizedBitmapResults:
        optimizedBitmapResults[i] = (optimizedBitmapResults[i]/repetitions)
    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples

    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    if PRINT_ALL:
    
        print "Amount of bytes: percentage of apperance " 
        print optimizedBitmapResults
    optimizedBitmap_summary_bytes_probability[bitmap_size] = optimizedBitmapResults
    if PRINT_ALL:
    
        print "bitmap_size:average ack size in bytes" 
        print str(optimizedBitmap_summary)
    #plt.show()
    


    '''
    print '\ninformation about the list of deltas'
    print "List of deltas -> Amount of bits: amount of times " 
    print str(list_of_deltas)
    print "Amount of bytes: amount of times " 
    print str(list_of_deltas_results_bytes[bitmap_size])
    average = 0
    provisional = 0
    provisional2 = 0
    for i in list_of_deltas_results_bytes[bitmap_size]:
        #print list_of_deltas[i]
        provisional = provisional + list_of_deltas_results_bytes[bitmap_size][i] * i
        provisional2 = provisional2 + list_of_deltas_results_bytes[bitmap_size][i]
        #print "provisional: " + str(provisional)
        #print "provisionsal2: " + str(provisional2)
    average = provisional / provisional2
    list_of_deltas_results_summary[bitmap_size] = average
    #for i in list_of_deltas_results_bytes[bitmap_size]:
    #    list_of_deltas_results_summary_bytes_probability[bitmap_size][i] = 100*(list_of_deltas_results_bytes[bitmap_size][i]/repetitions)
    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples

    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    #print "Amount of bits: percentage of apperance " 
    #print list_of_deltas_results_summary_bytes_probability
    print "bitmap_size:average ack size in bytes" 
    print str(list_of_deltas_results_summary)
    '''

    #SDNV-2
    ''' variance and standard deviation calculation '''
    print str(list_of_deltas_results_bytes_sdnv_2)
    sum_of_numbers = sum(number*count for number, count in list_of_deltas_results_bytes_sdnv_2[bitmap_size].iteritems())
    count = sum(count for n, count in list_of_deltas_results_bytes_sdnv_2[bitmap_size].iteritems())
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in list_of_deltas_results_bytes_sdnv_2[bitmap_size].iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    
    list_of_deltas_results_summary_sdnv_2_variance[bitmap_size] = variance
    list_of_deltas_results_summary_sdnv_2_sd[bitmap_size] = std_dev
    list_of_deltas_results_summary_sdnv_2[bitmap_size] = mean
    if PRINT_ALL:

        print '\ninformation about the list of deltas SDNV-2'
        print "List of deltas -> Amount of bits: amount of times " 
        print str(list_of_deltas_sdnv_2)
        print "Amount of bytes: amount of times " 
        print str(list_of_deltas_results_bytes_sdnv_2[bitmap_size])
    # average = 0
    # provisional = 0
    # provisional2 = 0
    # for i in list_of_deltas_results_bytes_sdnv_2[bitmap_size]:
    #     #print list_of_deltas[i]
    #     provisional = provisional + list_of_deltas_results_bytes_sdnv_2[bitmap_size][i] * i
    #     provisional2 = provisional2 + list_of_deltas_results_bytes_sdnv_2[bitmap_size][i]
    #     #print "provisional: " + str(provisional)
    #     #print "provisionsal2: " + str(provisional2)
    # average = provisional / provisional2
    # list_of_deltas_results_summary_sdnv_2[bitmap_size] = average
    list_of_deltas_results_summary_bytes_probability_sdnv_2_prob = defaultdict(float)
    for i in list_of_deltas_results_bytes_sdnv_2[bitmap_size]:
        list_of_deltas_results_summary_bytes_probability_sdnv_2_prob[i] = (list_of_deltas_results_bytes_sdnv_2[bitmap_size][i]/repetitions)
    list_of_deltas_results_summary_bytes_probability_sdnv_2[bitmap_size] = list_of_deltas_results_summary_bytes_probability_sdnv_2_prob
    if PRINT_ALL:
    
        print list_of_deltas_results_summary_bytes_probability_sdnv_2[bitmap_size]

    #print pdf_calculation(list_of_deltas_results_bytes_sdnv_2[bitmap_size],repetitions)
    
    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples

    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    if PRINT_ALL:
    
        print "Amount of bits: percentage of apperance " 
        print list_of_deltas_results_summary_bytes_probability_sdnv_2
        print "bitmap_size:average ack size in bytes" 
        print str(list_of_deltas_results_summary_sdnv_2)

    #SDNV-3
    ''' variance and standard deviation calculation '''
    sum_of_numbers = sum(number*count for number, count in list_of_deltas_results_bytes_sdnv_3[bitmap_size].iteritems())
    count = sum(count for n, count in list_of_deltas_results_bytes_sdnv_3[bitmap_size].iteritems())
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in list_of_deltas_results_bytes_sdnv_3[bitmap_size].iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    
    list_of_deltas_results_summary_sdnv_3_variance[bitmap_size] = variance
    list_of_deltas_results_summary_sdnv_3_sd[bitmap_size] = std_dev
    list_of_deltas_results_summary_sdnv_3[bitmap_size] = mean
    if PRINT_ALL:

        print '\ninformation about the list of deltas SDNV-3'
        print "List of deltas -> Amount of bits: amount of times " 
        print str(list_of_deltas_sdnv_3)
        print "Amount of bytes: amount of times " 
        print str(list_of_deltas_results_bytes_sdnv_3[bitmap_size])
    # average = 0
    # provisional = 0
    # provisional2 = 0
    # for i in list_of_deltas_results_bytes_sdnv_3[bitmap_size]:
    #     #print list_of_deltas[i]
    #     provisional = provisional + list_of_deltas_results_bytes_sdnv_3[bitmap_size][i] * i
    #     provisional2 = provisional2 + list_of_deltas_results_bytes_sdnv_3[bitmap_size][i]
    #     #print "provisional: " + str(provisional)
    #     #print "provisionsal2: " + str(provisional2)
    # average = provisional / provisional2
    # list_of_deltas_results_summary_sdnv_3[bitmap_size] = average
    list_of_deltas_results_summary_bytes_probability_sdnv_3_prob = defaultdict(float)

    for i in list_of_deltas_results_bytes_sdnv_3[bitmap_size]:
        list_of_deltas_results_summary_bytes_probability_sdnv_3_prob[i] = (list_of_deltas_results_bytes_sdnv_3[bitmap_size][i]/repetitions)
    list_of_deltas_results_summary_bytes_probability_sdnv_3[bitmap_size] = list_of_deltas_results_summary_bytes_probability_sdnv_3_prob
    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples

    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    if PRINT_ALL:

        print "Amount of bits: percentage of apperance " 
        print list_of_deltas_results_summary_bytes_probability_sdnv_3
        print "bitmap_size:average ack size in bytes" 
        print str(list_of_deltas_results_summary_sdnv_3)

    #SDNV-4
    ''' variance and standard deviation calculation '''
    sum_of_numbers = sum(number*count for number, count in list_of_deltas_results_bytes_sdnv_4[bitmap_size].iteritems())
    count = sum(count for n, count in list_of_deltas_results_bytes_sdnv_4[bitmap_size].iteritems())
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in list_of_deltas_results_bytes_sdnv_4[bitmap_size].iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    
    list_of_deltas_results_summary_sdnv_4_variance[bitmap_size] = variance
    list_of_deltas_results_summary_sdnv_4_sd[bitmap_size] = std_dev
    list_of_deltas_results_summary_sdnv_4[bitmap_size] = mean
    if PRINT_ALL:

        print '\ninformation about the list of deltas SDNV-4'
        print "List of deltas -> Amount of bits: amount of times " 
        print str(list_of_deltas_sdnv_4)
        print "Amount of bytes: amount of times " 
        print str(list_of_deltas_results_bytes_sdnv_4[bitmap_size])
    # average = 0
    # provisional = 0
    # provisional2 = 0
    # for i in list_of_deltas_results_bytes_sdnv_4[bitmap_size]:
    #     #print list_of_deltas[i]
    #     provisional = provisional + list_of_deltas_results_bytes_sdnv_4[bitmap_size][i] * i
    #     provisional2 = provisional2 + list_of_deltas_results_bytes_sdnv_4[bitmap_size][i]
    #     #print "provisional: " + str(provisional)
    #     #print "provisionsal2: " + str(provisional2)
    # average = provisional / provisional2
    # list_of_deltas_results_summary_sdnv_4[bitmap_size] = average
    list_of_deltas_results_summary_bytes_probability_sdnv_4_prob = defaultdict(float)

    for i in list_of_deltas_results_bytes_sdnv_4[bitmap_size]:
        list_of_deltas_results_summary_bytes_probability_sdnv_4_prob[i] = (list_of_deltas_results_bytes_sdnv_4[bitmap_size][i]/repetitions)
    list_of_deltas_results_summary_bytes_probability_sdnv_4[bitmap_size] = list_of_deltas_results_summary_bytes_probability_sdnv_4_prob
    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples

    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    if PRINT_ALL:

        print "Amount of bytes: percentage of apperance " 
        print list_of_deltas_results_summary_bytes_probability_sdnv_4
        print "bitmap_size:average ack size in bytes" 
        print str(list_of_deltas_results_summary_sdnv_4)

    #SDNV-5
    ''' variance and standard deviation calculation '''
    sum_of_numbers = sum(number*count for number, count in list_of_deltas_results_bytes_sdnv_5[bitmap_size].iteritems())
    count = sum(count for n, count in list_of_deltas_results_bytes_sdnv_5[bitmap_size].iteritems())
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in list_of_deltas_results_bytes_sdnv_5[bitmap_size].iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    
    list_of_deltas_results_summary_sdnv_5_variance[bitmap_size] = variance
    list_of_deltas_results_summary_sdnv_5_sd[bitmap_size] = std_dev
    list_of_deltas_results_summary_sdnv_5[bitmap_size] = mean
    if PRINT_ALL:
        print '\ninformation about the list of deltas SDNV-5'
        print "List of deltas -> Amount of bits: amount of times " 
        print str(list_of_deltas_sdnv_5)
        print "Amount of bytes: amount of times " 
        print str(list_of_deltas_results_bytes_sdnv_5[bitmap_size])
    # average = 0
    # provisional = 0
    # provisional2 = 0
    # for i in list_of_deltas_results_bytes_sdnv_5[bitmap_size]:
    #     #print list_of_deltas[i]
    #     provisional = provisional + list_of_deltas_results_bytes_sdnv_5[bitmap_size][i] * i
    #     provisional2 = provisional2 + list_of_deltas_results_bytes_sdnv_5[bitmap_size][i]
    #     #print "provisional: " + str(provisional)
    #     #print "provisionsal2: " + str(provisional2)
    # average = provisional / provisional2
    # list_of_deltas_results_summary_sdnv_5[bitmap_size] = average
    list_of_deltas_results_summary_bytes_probability_sdnv_5_prob = defaultdict(float)

    for i in list_of_deltas_results_bytes_sdnv_5[bitmap_size]:
        list_of_deltas_results_summary_bytes_probability_sdnv_5_prob[i] = (list_of_deltas_results_bytes_sdnv_5[bitmap_size][i]/repetitions)
    list_of_deltas_results_summary_bytes_probability_sdnv_5[bitmap_size] = list_of_deltas_results_summary_bytes_probability_sdnv_5_prob
    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples

    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    if PRINT_ALL:

        print "Amount of bytes: percentage of apperance " 
        print list_of_deltas_results_summary_bytes_probability_sdnv_5
        print "bitmap_size:average ack size in bytes" 
        print str(list_of_deltas_results_summary_sdnv_5)







    #LLF
    ''' variance and standard deviation calculation '''
    sum_of_numbers = sum(number*count for number, count in list_of_fragments_numbers_result_bytes[bitmap_size].iteritems())
    count = sum(count for n, count in list_of_fragments_numbers_result_bytes[bitmap_size].iteritems())
    mean = sum_of_numbers / count
    print mean
    total_squares = sum(number*number * count for number, count in list_of_fragments_numbers_result_bytes[bitmap_size].iteritems())
    mean_of_squares = total_squares / count
    variance = mean_of_squares - mean * mean
    std_dev = math.sqrt(variance)
    print variance
    print std_dev
    
    list_of_fragments_numbers_result_summary_variance[bitmap_size] = variance
    list_of_fragments_numbers_result_summary_sd[bitmap_size] = std_dev
    list_of_fragments_numbers_result_summary[bitmap_size] = mean
    if PRINT_ALL:

        print '\ninformation about the list of fragment number'
        print "Amount of bits: amount of times " 
        print str(list_of_fragments_numbers)
        print "Amount of bytes: amount of times " 
        print str(list_of_fragments_numbers_result_bytes[bitmap_size])
    
    # average = 0
    # provisional = 0
    # provisional2 = 0
    # for i in list_of_fragments_numbers_result_bytes[bitmap_size]:
    #     #print list_of_fragments_numbers[i]
    #     provisional = provisional + list_of_fragments_numbers_result_bytes[bitmap_size][i] * i
    #     provisional2 = provisional2 + list_of_fragments_numbers_result_bytes[bitmap_size][i]
    #     #print "provisional: " + str(provisional)
    #     #print "provisionsal2: " + str(provisional2)
    # average = provisional / provisional2
    # list_of_fragments_numbers_result_summary[bitmap_size] = average
    #print list_of_fragments_numbers_result_bytes[bitmap_size]
    list_of_fragments_numbers_result_summary_bytes_probability_prob = defaultdict(float)
    for i in list_of_fragments_numbers_result_bytes[bitmap_size]:
    #    print str(i) + ', ' + str(list_of_fragments_numbers_result_bytes[bitmap_size][i])
        list_of_fragments_numbers_result_summary_bytes_probability_prob[i] = (list_of_fragments_numbers_result_bytes[bitmap_size][i]/repetitions)
    list_of_fragments_numbers_result_summary_bytes_probability[bitmap_size] = list_of_fragments_numbers_result_summary_bytes_probability_prob

    #plt.figure(3)
    #lists = sorted(optimizedBitmapResults.items()) # sorted by key, return a list of tuples
    #x, y = zip(*lists) # unpack a list of pairs into two tuples
    #plt.bar(x, y)
    if PRINT_ALL:

        print "Amount of bytes: percentage of apperance " 
        print list_of_fragments_numbers_result_summary_bytes_probability
        print "bitmap_size:average ack size in bytes" 
        print str(list_of_fragments_numbers_result_summary)


    '''bitmap_size + bitmap_delta'''
    bitmap_size = bitmap_size + bitmap_delta



'''
plt.figure(3)
lists = sorted(optimizedBitmap_summary.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.bar(x, y)
plt.xticks(x,x)
plt.title("Average bytes in ack optimized bitmap") 
plt.xlabel("bitmap size") 
plt.ylabel("Size of ack (bytes)") 
##plt.show()
'''
'''UNCOMMENT FOR INDIVIDUAL PRINTING
for i in sorted(optimizedBitmap_summary):
    print str(i) + "," + str(optimizedBitmap_summary[i])
print 'list_of_deltas_results_summary'
for i in sorted(list_of_deltas_results_summary):
    print str(i) + "," + str(list_of_deltas_results_summary[i])

##print list_of_deltas_results_summary
print 'list_of_fragments_numbers_result_summary'
for i in sorted(list_of_fragments_numbers_result_summary):
    print str(i) + "," + str(list_of_fragments_numbers_result_summary[i])
#print list_of_fragments_numbers_result_summary
'''

print 'Summary averague ack in bytes'
#print 'bitmap size, optimized Bitmap, SDNV, list of fragments number, probability'
#for i in sorted(optimizedBitmap_summary):
#    print str(i) + "," + str(optimizedBitmap_summary[i]) + "," + str(list_of_deltas_results_summary[i]) + "," + str(list_of_fragments_numbers_result_summary[i]) +"," + str(probability_total_summary[i])

print 'bitmap size, bitmap'
for i in sorted(Bitmap_summary):
    print str(i) + "," + str(Bitmap_summary[i])

print 'bitmap size, compressed Bitmap, list of fragments number, SDNV-2, SDNV-3, SDNV-4, SDNV-5, probability'
for i in sorted(optimizedBitmap_summary):
    print str(i) + "," + str(optimizedBitmap_summary[i]) + "," + str(list_of_fragments_numbers_result_summary[i]) +"," + str(list_of_deltas_results_summary_sdnv_2[i]) + ","+ str(list_of_deltas_results_summary_sdnv_3[i]) + ","+str(list_of_deltas_results_summary_sdnv_4[i]) + ","+str(list_of_deltas_results_summary_sdnv_5[i]) + ","+ str(probability_total_summary[i])
if PRINT_PDF:
    print 'compressed Bitmap'
    #print optimizedBitmap_summary_bytes_probability
    for i in sorted(optimizedBitmap_summary_bytes_probability):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(optimizedBitmap_summary_bytes_probability[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(optimizedBitmap_summary_bytes_probability[i]):
            print str(optimizedBitmap_summary_bytes_probability[i][byte_size]) + ",",
        print
        
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i]) + "," + str(list_of_fragments_numbers_result_summary[i]) +"," + str(list_of_deltas_results_summary_sdnv_2[i]) + ","+ str(list_of_deltas_results_summary_sdnv_3[i]) + ","+str(list_of_deltas_results_summary_sdnv_4[i]) + ","+str(list_of_deltas_results_summary_sdnv_5[i]) + ","+ str(probability_total_summary[i])


    print 'SDNV-2'
    for i in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_2):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_2[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_2[i]):
            print str(list_of_deltas_results_summary_bytes_probability_sdnv_2[i][byte_size]) + ",",
        print

    print 'SNDV-3'
    for i in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_3):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_3[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_3[i]):
            print str(list_of_deltas_results_summary_bytes_probability_sdnv_3[i][byte_size]) + ",",
        print

    print 'SDNV-4'
    for i in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_4):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_4[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_4[i]):
            print str(list_of_deltas_results_summary_bytes_probability_sdnv_4[i][byte_size]) + ",",
        print


    print 'SDNV-5'
    for i in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_5):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_5[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_results_summary_bytes_probability_sdnv_5[i]):
            print str(list_of_deltas_results_summary_bytes_probability_sdnv_5[i][byte_size]) + ",",
        print


    print 'list of fragments'
    for i in sorted(list_of_fragments_numbers_result_summary_bytes_probability):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_fragments_numbers_result_summary_bytes_probability[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_fragments_numbers_result_summary_bytes_probability[i]):
            print str(list_of_fragments_numbers_result_summary_bytes_probability[i][byte_size]) + ",",
        print



'''
plt.figure(1)
lists = sorted(list_of_deltas_results_summary.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.bar(x, y)
plt.xticks(x,x)
plt.title("Average bits in ack list of deltas") 
plt.xlabel("bitmap size") 
plt.ylabel("Size of ack (bytes)") 
#plt.show()
'''
'''
plt.figure(2)
print list_of_fragments_numbers_result_summary
lists = sorted(list_of_fragments_numbers_result_summary.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.bar(x, y)
plt.xticks(x,x)
plt.title("Average bits in ack list of fragments numbers") 
plt.xlabel("bitmap size") 
plt.ylabel("Size of ack (bytes)") 
#plt.show()


plt.figure(5)
print probability_total_summary
lists = sorted(probability_total_summary.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.bar(x, y)
plt.xticks(x,x)
plt.title("probability_total_summary") 
plt.xlabel("bitmap size") 
plt.ylabel("Size of ack (bytes)") 
#plt.show()
'''
print 'list_of_deltas_results_bits*'
#print list_of_deltas_results_bits
#if DELTA_BASE_SIZE == 4:
#    print 'base'
#    for i in sorted(list_of_deltas_results_bits):
#        print str(i) + ", " + str(list_of_deltas_results_bits[i][4]/(list_of_deltas_results_bits[i][4]+list_of_deltas_results_bits[i][8]+list_of_deltas_results_bits[i][12])) + ", " + str(list_of_deltas_results_bits[i][8]/(list_of_deltas_results_bits[i][4]+list_of_deltas_results_bits[i][8]+list_of_deltas_results_bits[i][12])) + ", " + str(list_of_deltas_results_bits[i][12]/(list_of_deltas_results_bits[i][4]+list_of_deltas_results_bits[i][8]+list_of_deltas_results_bits[i][12]))
'''
        plt.figure(6+i)
        lists = sorted(list_of_deltas_results_bits[i].items()) # sorted by key, return a list of tuples

        x, y = zip(*lists) # unpack a list of pairs into two tuples
        plt.bar(x, y)
        plt.xticks(x,x)
        plt.title("Delta bits size apearence (Total Delta)") 
        plt.xlabel("Size of delta (bits)") 
        plt.ylabel("number of appearence")
'''
print 'probability_total_summary'
for i in probability_total_summary:

    print str(i) +"," + str(probability_total_summary[i])

print 'list_of_deltas_real_results_summary_bits'
'''
print 'bitmap size, real delta value, amount'
for i in sorted(list_of_deltas_real_results_summary_bits):
    print str(i)+', ' ,
    #for deltaRealSize in list_of_deltas_real_results_summary_bits[i]:
    #    print str(deltaRealSize)+", ",
    for deltaRealSize in sorted(list_of_deltas_real_results_summary_bits[i]):
        print str(list_of_deltas_real_results_summary_bits[i][deltaRealSize])+", ",
    print
'''
#plt.show()
#print "bitmap_size:average ack size in bytes" 
#print str(list_of_deltas_results_summary)





print "------------------FRAMES ------------------------"
print 'Summary averague ack in bytes'
#print 'bitmap size, optimized Bitmap, SDNV, list of fragments number, probability'
#for i in sorted(optimizedBitmap_summary):
#    print str(i) + "," + str(optimizedBitmap_summary[i]) + "," + str(list_of_deltas_results_summary[i]) + "," + str(list_of_fragments_numbers_result_summary[i]) +"," + str(probability_total_summary[i])

print 'bitmap size, bitmap'
for i in sorted(bitmap_results_frames_lora_prob):
    print str(i) + "," + str(bitmap_results_frames_lora_prob[i])

print 'bitmap size, compressed Bitmap, list of fragments number, SDNV-2, SDNV-3, SDNV-4, SDNV-5, probability'
for i in sorted(list_of_fragments_numbers_results_frames_lora_prob):
    print str(i) + "," + str(compressed_bitmap_results_frames_lora_prob[i]) + "," + str(list_of_fragments_numbers_results_frames_lora_prob[i]) +"," + str(list_of_deltas_sdnv_2_results_frames_lora_prob[i]) + ","+ str(list_of_deltas_sdnv_3_results_frames_lora_prob[i]) + ","+str(list_of_deltas_sdnv_4_results_frames_lora_prob[i]) + ","+str(list_of_deltas_sdnv_5_results_frames_lora_prob[i]) + ","+ str(probability_total_summary[i])

if PRINT_PDF:
    print 'compressed Bitmap'
    #print optimizedBitmap_summary_bytes_probability
    for i in sorted(compressed_bitmap_results_frames_lora_pdf):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(compressed_bitmap_results_frames_lora_pdf[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(compressed_bitmap_results_frames_lora_pdf[i]):
            print str(compressed_bitmap_results_frames_lora_pdf[i][byte_size]) + ",",
        print
        
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i]) + "," + str(list_of_fragments_numbers_result_summary[i]) +"," + str(list_of_deltas_results_summary_sdnv_2[i]) + ","+ str(list_of_deltas_results_summary_sdnv_3[i]) + ","+str(list_of_deltas_results_summary_sdnv_4[i]) + ","+str(list_of_deltas_results_summary_sdnv_5[i]) + ","+ str(probability_total_summary[i])


    print 'SDNV-2'
    for i in sorted(list_of_deltas_sdnv_2_results_frames_lora_pdf):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_sdnv_2_results_frames_lora_pdf[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_sdnv_2_results_frames_lora_pdf[i]):
            print str(list_of_deltas_sdnv_2_results_frames_lora_pdf[i][byte_size]) + ",",
        print

    print 'SNDV-3'
    for i in sorted(list_of_deltas_sdnv_3_results_frames_lora_pdf):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_sdnv_3_results_frames_lora_pdf[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_sdnv_3_results_frames_lora_pdf[i]):
            print str(list_of_deltas_sdnv_3_results_frames_lora_pdf[i][byte_size]) + ",",
        print

    print 'SDNV-4'
    for i in sorted(list_of_deltas_sdnv_4_results_frames_lora_pdf):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_sdnv_4_results_frames_lora_pdf[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_sdnv_4_results_frames_lora_pdf[i]):
            print str(list_of_deltas_sdnv_4_results_frames_lora_pdf[i][byte_size]) + ",",
        print


    print 'SDNV-5'
    for i in sorted(list_of_deltas_sdnv_5_results_frames_lora_pdf):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_deltas_sdnv_5_results_frames_lora_pdf[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_deltas_sdnv_5_results_frames_lora_pdf[i]):
            print str(list_of_deltas_sdnv_5_results_frames_lora_pdf[i][byte_size]) + ",",
        print


    print 'list of fragments'
    for i in sorted(list_of_fragments_numbers_results_frames_lora_pdf):
        #print str(i) + "," + str(optimizedBitmap_summary_bytes_probability[i])
        print str(i)+ ","
        for byte_size in sorted(list_of_fragments_numbers_results_frames_lora_pdf[i]):
            print str(byte_size) + ",", #+ str(optimizedBitmap_summary_bytes_probability[i][byte_size]),
        print 
        for byte_size in sorted(list_of_fragments_numbers_results_frames_lora_pdf[i]):
            print str(list_of_fragments_numbers_results_frames_lora_pdf[i][byte_size]) + ",",
        print

print 'FER -> ' + str(FER*100) + '%'
print 'FER_RANDOM ->' +str(FER_RANDOM) + '%'
print 'poisson_lambda -> ' + str(poisson_lambda)
print "BITMAP_GENERATION = "+  BITMAP_GENERATION
print 'list_of_fragments_numbers_lenght = ' + str(list_of_fragments_numbers_lenght) 
print 'bitmap_size = ' + str(bitmap_size)
print 'bitmap_size_max = ' + str(bitmap_size_max)
print 'bitmap_delta = ' + str(bitmap_delta)
print 'repetitions =' + str(repetitions) 



logtime = datetime.datetime.now()
date = ""
date = date + str(logtime.day)
date = date +"-" + str(logtime.month)
date = date + "-" + str(logtime.year) + "_"
date = date + str(logtime.hour)
date = date + "" + str(logtime.minute)
date = date + "" + str(logtime.second)
save_path = save_path + date+ "_"
if BITMAP_GENERATION == 'BURST':
    file1_name = BITMAP_GENERATION + '_FER_' + str(FER*100)+ '_lambda_' + str(poisson_lambda)+ '.tex' 
    '''file for frames size'''
    file1 = open(save_path + 'frames_'+file1_name, "w")
    file1.write('\\begin{tikzpicture}\n')
    file1.write('\\begin{axis}[\n')
    file1.write('title=Average Frame size vs packet size'+' (Burst Errors '+str(FER*100)+'\% '+str(poisson_lambda)+' average burst)'+',\n')
    file1.write('xlabel=Packet size (fragments),\n')
    file1.write('ylabel=Average number of Frames\n')
    file1.write(',legend style ={at ={(1.8,1)}}, anchor=north east')
    file1.write(']\n')
    
    '''file for Ack size'''
    file2 = open(save_path + 'ack_size_'+file1_name, "w")
    file2.write('\\begin{tikzpicture}\n')
    file2.write('\\begin{axis}[\n')
    file2.write('title=Average Ack size vs packet size'+' (Burst Errors '+str(FER*100)+'\% '+str(poisson_lambda)+' average burst)'+',\n')
    file2.write('xlabel=Packet size (fragments),\n')
    file2.write('ylabel=Average Ack Size (bytes)\n')
    file2.write(',legend style ={at ={(1.8,1)}}, anchor=north east')
    file2.write(']\n')

    
    
    '''file for TOA'''
    file3 = open(save_path + 'TOA_'+file1_name, "w")
    file3.write('\\begin{tikzpicture}\n')
    file3.write('\\begin{axis}[\n')
    file3.write('title=Average TOA vs packet size'+' (Burst Errors '+str(FER*100)+'\% '+str(poisson_lambda)+' average burst)'+',\n')
    file3.write('xlabel=Packet size (fragments),\n')
    file3.write('ylabel=TOA (s)\n')
    file3.write(',legend style ={at ={(1.8,1)}}, anchor=north east')
    file3.write(']\n')

    '''file for TOA_GAIN'''
    file4 = open(save_path + 'TOA_GAIN_'+file1_name, "w")
    file4.write('\\begin{tikzpicture}\n')
    file4.write('\\begin{axis}[\n')
    file4.write('title=Average TOA_GAIN vs packet size'+' (Burst Errors '+str(FER*100)+'\% '+str(poisson_lambda)+' average burst)'+',\n')
    file4.write('xlabel=Packet size (fragments),\n')
    file4.write('ylabel=TOA GAIN (\%)\n,')
    file4.write('legend style={font=\small, legend pos=outer north east}\n,')
    file4.write('legend columns = 1\n,')
    file4.write('cycle list name = \mylistBitmapTOAGAIN\n,')
    file4.write('grid = major\n,')
    file4.write('log ticks with fixed point\n,')
    file4.write('every axis legend/.append style={nodes={right}}\n,')
    file4.write('mark options = {solid, scale =1.2}\n')
    file4.write(']\n')
    

else:
    file1_name = BITMAP_GENERATION + '_FER_' + str(FER_RANDOM) + '.tex' 
    '''file for frames size'''
    file1 = open(save_path + 'frames_'+file1_name, "w")
    file1.write('\\begin{tikzpicture}\n')
    file1.write('\\begin{axis}[\n')
    file1.write('title=Average Frame size vs packet size'+'(Random Errors '+str(FER_RANDOM)+'\%)'+',\n')
    file1.write('xlabel=Packet size (fragments),\n')
    file1.write('ylabel=Average number of Frames\n')
    file1.write(',legend style ={at ={(1.8,1)}}, anchor=north east')
    file1.write(']\n')
    
    '''file for Ack size'''
    file2 = open(save_path + 'ack_size_'+file1_name, "w")
    file2.write('\\begin{tikzpicture}\n')
    file2.write('\\begin{axis}[\n')
    file2.write('title=Average Ack size vs packet size'+' (Random Errors '+str(FER_RANDOM)+'\%)'+',\n')
    file2.write('xlabel=Packet size (fragments),\n')
    file2.write('ylabel=Average Ack Size (bytes)\n')
    file2.write(',legend style ={at ={(1.8,1)}}, anchor=north east')
    file2.write(']\n')

    
    
    '''file for TOA'''
    file3 = open(save_path + 'TOA_'+file1_name, "w")
    file3.write('\\begin{tikzpicture}\n')
    file3.write('\\begin{axis}[\n')
    file3.write('title=Average TOA vs packet size'+' (Random Errors '+str(FER_RANDOM)+'\%)'+',\n')
    file3.write('xlabel=Packet size (fragments),\n')
    file3.write('ylabel=TOA (s)\n')
    file3.write(',legend style ={at ={(1.8,1)}}, anchor=north east')
    file3.write(']\n')

    '''file for TOA_GAIN'''
    file4 = open(save_path + 'TOA_GAIN_'+file1_name, "w")
    file4.write('\\begin{tikzpicture}\n')
    file4.write('\\begin{axis}[\n')
    file4.write('title=Average TOA GAIN vs packet size'+' (Random Errors '+str(FER_RANDOM)+'\%)'+',\n')
    file4.write('xlabel=Packet size (fragments),\n')
    file4.write('ylabel=TOA GAIN (\%)\n,')
    file4.write('legend style={font=\small, legend pos=outer north east}\n,')
    file4.write('legend columns = 1\n,')
    file4.write('cycle list name = \mylistBitmapTOAGAIN\n,')
    file4.write('grid = major\n,')
    file4.write('log ticks with fixed point\n,')
    file4.write('every axis legend/.append style={nodes={right}}\n,')
    file4.write('mark options = {solid, scale =1.2}\n')
    file4.write(']\n')


if WRITE_TO_file:
    #file1 = open(file1_name, "w")
    #file1.write('\\begin{tikzpicture}\n')
    #file1.write('\\begin{axis}[\n')
    #file1.write('title=Average Frame size vs packet size'+''+',\n')
    #file1.write('xlabel=$P_{success}$,\n')
    #file1.write('ylabel=Ack\_bits\_per\_data\_bit\n')
    #file1.write(']\n')
    file1.write( "%BITMAP_GENERATION = "+  BITMAP_GENERATION+ '\n')
    file1.write( '%list_of_fragments_numbers_lenght = ' + str(list_of_fragments_numbers_lenght)+ '\n') 
    file1.write( '%bitmap_size = ' + str(bitmap_size)+ '\n')
    file1.write( '%bitmap_size_max = ' + str(bitmap_size_max)+ '\n')
    file1.write( '%bitmap_delta = ' + str(bitmap_delta)+ '\n')
    file1.write( '%repetitions =' + str(repetitions)+ '\n') 


    file2.write( "%BITMAP_GENERATION = "+  BITMAP_GENERATION+ '\n')
    file2.write( '%list_of_fragments_numbers_lenght = ' + str(list_of_fragments_numbers_lenght)+ '\n') 
    file2.write( '%bitmap_size = ' + str(bitmap_size)+ '\n')
    file2.write( '%bitmap_size_max = ' + str(bitmap_size_max)+ '\n')
    file2.write( '%bitmap_delta = ' + str(bitmap_delta)+ '\n')
    file2.write( '%repetitions =' + str(repetitions)+ '\n')

    file3.write( "%BITMAP_GENERATION = "+  BITMAP_GENERATION+ '\n')
    file3.write( '%list_of_fragments_numbers_lenght = ' + str(list_of_fragments_numbers_lenght)+ '\n') 
    file3.write( '%bitmap_size = ' + str(bitmap_size)+ '\n')
    file3.write( '%bitmap_size_max = ' + str(bitmap_size_max)+ '\n')
    file3.write( '%bitmap_delta = ' + str(bitmap_delta)+ '\n')
    file3.write( '%repetitions =' + str(repetitions)+ '\n')




    if BITMAP_GENERATION == 'BURST':
        file1.write( '%FER -> ' + str(FER*100) + '%' + '\n')
        file1.write( '%poisson_lambda -> ' + str(poisson_lambda)+ '\n')
        
        file2.write( '%FER -> ' + str(FER*100) + '%' + '\n')
        file2.write( '%poisson_lambda -> ' + str(poisson_lambda)+ '\n')

        file3.write( '%FER -> ' + str(FER*100) + '%' + '\n')
        file3.write( '%poisson_lambda -> ' + str(poisson_lambda)+ '\n')
        
        file4.write( '%FER -> ' + str(FER*100) + '%' + '\n')
        file4.write( '%poisson_lambda -> ' + str(poisson_lambda)+ '\n')


    else:
        file1.write( '%FER_RANDOM ->' +str(FER_RANDOM) + '%'+ '\n')
    
        file2.write( '%FER_RANDOM ->' +str(FER_RANDOM) + '%'+ '\n')

        file3.write( '%FER_RANDOM ->' +str(FER_RANDOM) + '%'+ '\n')
        
        file4.write( '%FER_RANDOM ->' +str(FER_RANDOM) + '%'+ '\n')



    file1.write( "%------------------FRAMES ------------------------" + '\n')
    file1.write( '%Frames' + '\n')
    file1.write( '%bitmap size, compressed Bitmap, list of fragments number, SDNV-2, SDNV-3, SDNV-4, SDNV-5, probability' + '\n')
    
    file1.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_frames_lora_prob):
        file1.write( '(' + str(i) + ',' + str(bitmap_results_frames_lora_prob[i]) + ') +- (0,'+str(bitmap_results_frames_lora_sd[i])+')\n')      
    file1.write('};\n')
    file1.write('\\addlegendentry{Bitmap'+'}\n')  

    file1.write('\\addplot coordinates {\n')
    for i in sorted(list_of_fragments_numbers_results_frames_lora_prob):
        file1.write( '(' + str(i) + ',' + str(list_of_fragments_numbers_results_frames_lora_prob[i]) + ') +- (0,'+str(list_of_fragments_numbers_results_frames_lora_sd[i])+')\n')  
    file1.write('};\n')
    file1.write('\\addlegendentry{LLF'+'}\n')
    
    file1.write('\\addplot coordinates {\n')
    for i in sorted(compressed_bitmap_results_frames_lora_prob):
        file1.write( '(' + str(i) + ',' + str(compressed_bitmap_results_frames_lora_prob[i]) + ') +- (0,'+str(compressed_bitmap_results_frames_lora_sd[i])+')\n')     
    file1.write('};\n')
    file1.write('\\addlegendentry{CB'+'}\n')    
    
    file1.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_2_results_frames_lora_prob):
        file1.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_2_results_frames_lora_prob[i]) + ') +- (0,'+str(list_of_deltas_sdnv_2_results_frames_lora_sd[i])+')\n') 
    file1.write('};\n')
    file1.write('\\addlegendentry{LoD-2'+'}\n')

    file1.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_3_results_frames_lora_prob):
        file1.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_3_results_frames_lora_prob[i]) + ') +- (0,'+str(list_of_deltas_sdnv_3_results_frames_lora_sd[i])+')\n')    
    file1.write('};\n')
    file1.write('\\addlegendentry{LoD-3'+'}\n')

    file1.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_4_results_frames_lora_prob):
        file1.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_4_results_frames_lora_prob[i]) + ') +- (0,'+str(list_of_deltas_sdnv_4_results_frames_lora_sd[i])+')\n')      
    file1.write('};\n')
    file1.write('\\addlegendentry{LoD-4'+'}\n')

    file1.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_5_results_frames_lora_prob):
        file1.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_5_results_frames_lora_prob[i]) + ') +- (0,'+str(list_of_deltas_sdnv_5_results_frames_lora_sd[i])+')\n')       
    file1.write('};\n')
    file1.write('\\addlegendentry{LoD-5'+'}\n')

    file1.write('\\end{axis}' + '\n')
    file1.write('\\end{tikzpicture}' + '\n')
    file1.close()
    #for i in sorted(list_of_fragments_numbers_results_frames_lora_prob):       
    #    file1.write( str(i) + "," + str(compressed_bitmap_results_frames_lora_prob[i]) + "," + str(list_of_fragments_numbers_results_frames_lora_prob[i]) +"," + str(list_of_deltas_sdnv_2_results_frames_lora_prob[i]) + ","+ str(list_of_deltas_sdnv_3_results_frames_lora_prob[i]) + ","+str(list_of_deltas_sdnv_4_results_frames_lora_prob[i]) + ","+str(list_of_deltas_sdnv_5_results_frames_lora_prob[i]) + ","+ str(probability_total_summary[i]) + '\n')    




    file2.write( "%------------------ACKS ------------------------" + '\n')
    file2.write( '%Acks' + '\n')
    file2.write( '%bitmap size, compressed Bitmap, list of fragments number, SDNV-2, SDNV-3, SDNV-4, SDNV-5, probability' + '\n')
    #for i in sorted(optimizedBitmap_summary):
    #    file1.write( str(i) + "," + str(optimizedBitmap_summary[i]) + "," + str(list_of_fragments_numbers_result_summary[i]) +"," + str(list_of_deltas_results_summary_sdnv_2[i]) + ","+ str(list_of_deltas_results_summary_sdnv_3[i]) + ","+str(list_of_deltas_results_summary_sdnv_4[i]) + ","+str(list_of_deltas_results_summary_sdnv_5[i]) + ","+ str(probability_total_summary[i]) + '\n')
    
    file2.write('\\addplot[error bars/.cd] coordinates {\n')
    for i in sorted(Bitmap_summary):
        file2.write( '(' + str(i) + ',' + str(Bitmap_summary[i]) + ') +- (0,'+str(Bitmap_summary_sd[i])+')\n')    
    file2.write('};\n')
    file2.write('\\addlegendentry{Bitmap'+'}\n')  
    
    file2.write('\\addplot coordinates {\n')
    for i in sorted(list_of_fragments_numbers_result_summary):
        file2.write( '(' + str(i) + ',' + str(list_of_fragments_numbers_result_summary[i])+ ') +- (0,'+str(list_of_fragments_numbers_result_summary_sd[i])+')\n') 
    file2.write('};\n')
    file2.write('\\addlegendentry{LLF'+'}\n')
    
    file2.write('\\addplot coordinates {\n')
    for i in sorted(optimizedBitmap_summary):
        file2.write( '(' + str(i) + ',' + str(optimizedBitmap_summary[i]) + ') +- (0,'+str(optimizedBitmap_summary_sd[i])+')\n')    
    file2.write('};\n')
    file2.write('\\addlegendentry{CB'+'}\n')    
    
    file2.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_results_summary_sdnv_2):
        file2.write( '(' + str(i) + ',' + str(list_of_deltas_results_summary_sdnv_2[i]) + ') +- (0,'+str(list_of_deltas_results_summary_sdnv_2_sd[i])+')\n')      
    file2.write('};\n')
    file2.write('\\addlegendentry{LoD-2'+'}\n')

    file2.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_results_summary_sdnv_3):
        file2.write( '(' + str(i) + ',' + str(list_of_deltas_results_summary_sdnv_3[i]) + ') +- (0,'+str(list_of_deltas_results_summary_sdnv_3_sd[i])+')\n')   
    file2.write('};\n')
    file2.write('\\addlegendentry{LoD-3'+'}\n')

    file2.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_results_summary_sdnv_4):
        file2.write( '(' + str(i) + ',' + str(list_of_deltas_results_summary_sdnv_4[i]) + ') +- (0,'+str(list_of_deltas_results_summary_sdnv_4_sd[i])+')\n')   
    file2.write('};\n')
    file2.write('\\addlegendentry{LoD-4'+'}\n')

    file2.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_results_summary_sdnv_5):
        file2.write( '(' + str(i) + ',' + str(list_of_deltas_results_summary_sdnv_5[i]) + ') +- (0,'+str(list_of_deltas_results_summary_sdnv_5_sd[i])+')\n')    
    file2.write('};\n')
    file2.write('\\addlegendentry{LoD-5'+'}\n')

    file2.write('\\end{axis}' + '\n')
    file2.write('\\end{tikzpicture}' + '\n')
    file2.close()





    file3.write( "%------------------TOA ------------------------" + '\n')
    file3.write( '%TOA' + '\n')
    file3.write( '%bitmap size, compressed Bitmap, list of fragments number, SDNV-2, SDNV-3, SDNV-4, SDNV-5, probability' + '\n')
    #for i in sorted(list_of_fragments_numbers_results_TOA):
    #    file1.write( str(i) + "," + str(compressed_bitmap_results_TOA[i]) + "," + str(list_of_fragments_numbers_results_TOA[i]) +"," + str(list_of_deltas_sdnv_2_results_TOA[i]) + ","+ str(list_of_deltas_sdnv_3_results_TOA[i]) + ","+str(list_of_deltas_sdnv_4_results_TOA[i]) + ","+str(list_of_deltas_sdnv_5_results_TOA[i]) + ","+ str(probability_total_summary[i]) + '\n')

    file3.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_TOA):
        file3.write( '(' + str(i) + ',' + str(bitmap_results_TOA[i]) + ') +- (0,'+str(bitmap_results_TOA_sd[i])+')\n')    
    file3.write('};\n')
    file3.write('\\addlegendentry{Bitmap'+'}\n')  

    file3.write('\\addplot coordinates {\n')
    for i in sorted(list_of_fragments_numbers_results_TOA):
        file3.write( '(' + str(i) + ',' + str(list_of_fragments_numbers_results_TOA[i]) + ') +- (0,'+str(list_of_fragments_numbers_results_TOA_sd[i])+')\n')    
    file3.write('};\n')
    file3.write('\\addlegendentry{LLF'+'}\n')
    
    file3.write('\\addplot coordinates {\n')
    for i in sorted(compressed_bitmap_results_TOA):
        file3.write( '(' + str(i) + ',' + str(compressed_bitmap_results_TOA[i]) + ') +- (0,'+str(compressed_bitmap_results_TOA_sd[i])+')\n')   
    file3.write('};\n')
    file3.write('\\addlegendentry{CB'+'}\n')    
    
    file3.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_2_results_TOA):
        file3.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_2_results_TOA[i]) + ') +- (0,'+str(list_of_deltas_sdnv_2_results_TOA_sd[i])+')\n')    
    file3.write('};\n')
    file3.write('\\addlegendentry{LoD-2'+'}\n')

    file3.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_3_results_TOA):
        file3.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_3_results_TOA[i]) + ') +- (0,'+str(list_of_deltas_sdnv_3_results_TOA_sd[i])+')\n')     
    file3.write('};\n')
    file3.write('\\addlegendentry{LoD-3'+'}\n')

    file3.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_4_results_TOA):
        file3.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_4_results_TOA[i]) + ') +- (0,'+str(list_of_deltas_sdnv_4_results_TOA_sd[i])+')\n')        
    file3.write('};\n')
    file3.write('\\addlegendentry{LoD-4'+'}\n')

    file3.write('\\addplot coordinates {\n')
    for i in sorted(list_of_deltas_sdnv_5_results_TOA):
        file3.write( '(' + str(i) + ',' + str(list_of_deltas_sdnv_5_results_TOA[i]) + ') +- (0,'+str(list_of_deltas_sdnv_5_results_TOA_sd[i])+')\n')      
    file3.write('};\n')
    file3.write('\\addlegendentry{LoD-5'+'}\n')

    file3.write('\\end{axis}' + '\n')
    file3.write('\\end{tikzpicture}' + '\n')
    file3.close()


    file4.write( "%------------------TOA GAIN------------------------" + '\n')
    file4.write( '%TOA GAIN' + '\n')

    # file4.write('\\addplot coordinates {\n')
    # for i in sorted(bitmap_results_TOA):
    #     file3.write( '(' + str(i) + ',' + str(bitmap_results_TOA[i]) + ') +- (0,'+str(bitmap_results_TOA_sd[i])+')\n')    
    # file3.write('};\n')
    # file3.write('\\addlegendentry{Bitmap'+'}\n')  

    file4.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_TOA):
        file4.write( '(' + str(i) + ',' + str(((bitmap_results_TOA[i] - list_of_fragments_numbers_results_TOA[i]) / bitmap_results_TOA[i])*100) +')\n')   
    file4.write('};\n')
    file4.write('\\addlegendentry{LLF'+'}\n')


    file4.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_TOA):
        file4.write( '(' + str(i) + ',' + str(((bitmap_results_TOA[i] - compressed_bitmap_results_TOA[i]) / bitmap_results_TOA[i])*100) +')\n')   
    file4.write('};\n')
    file4.write('\\addlegendentry{CB'+'}\n')


    file4.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_TOA):
        file4.write( '(' + str(i) + ',' + str(((bitmap_results_TOA[i] - list_of_deltas_sdnv_2_results_TOA[i]) / bitmap_results_TOA[i])*100) +')\n')   
    file4.write('};\n')
    file4.write('\\addlegendentry{LoD-2'+'}\n')


    file4.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_TOA):
        file4.write( '(' + str(i) + ',' + str(((bitmap_results_TOA[i] - list_of_deltas_sdnv_3_results_TOA[i]) / bitmap_results_TOA[i])*100) +')\n')   
    file4.write('};\n')
    file4.write('\\addlegendentry{LoD-3'+'}\n')


    file4.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_TOA):
        file4.write( '(' + str(i) + ',' + str(((bitmap_results_TOA[i] - list_of_deltas_sdnv_4_results_TOA[i]) / bitmap_results_TOA[i])*100) +')\n')   
    file4.write('};\n')
    file4.write('\\addlegendentry{LoD-4'+'}\n')
    file4.write('\\addplot coordinates {\n')
    for i in sorted(bitmap_results_TOA):
        file4.write( '(' + str(i) + ',' + str(((bitmap_results_TOA[i] - list_of_deltas_sdnv_5_results_TOA[i]) / bitmap_results_TOA[i])*100) +')\n')   
    file4.write('};\n')
    file4.write('\\addlegendentry{LoD-5'+'}\n')



    file4.write('\\end{axis}' + '\n')
    file4.write('\\end{tikzpicture}' + '\n')
    file4.close()


    #file1.close()