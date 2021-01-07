# Sim-RFT guide

To run the sim-RFT simulator follow this steps:
 
 1. Clone [this](https://github.com/saguilarDevel/sim-RFT.git) repository. 

 2. Install python 2.7.

 3. Install required libs in the requirements.txt, basically numpy must be installed.

 4. Find the sim-RFT.py file.
 
 5. Run in command line: 
    ```text
        python2.7 sim-RFT.py
    ``` 
    
 ### Configuration Guide
 
 In this section, an overview of the configuration of the sim-RFT is provided.
 
 
 #### Configuration parameters
  
  The following are the configuration parameters of sim-RFT.
  The bitmap generation variables indicates whether RANDOM or BURST errors are generated.
  
 ```python
    '''Sim-RFT Configuration values'''
    RANDOM = 'RANDOM'
    BURST = 'BURST'
    #Bitmap generation mode
    BITMAP_GENERATION = BURST
    #Size of FN for the List of Lost Fragments
    list_of_fragments_numbers_lenght = 7 #bits
    #Min bitmap size in simulation
    bitmap_size = 10
    #Max bitmap size in simulation
    bitmap_size_max = 12
    #delta in simulation
    bitmap_delta = 1
    #Number of simulations
    repetitions = 1000000
    #LoRa Payload size (frame size - ack headers)
    #frame size = 11 bytes, ACK headers = 1 byte
    LORA_PAYLOAD = 10
    SIGFOX_PAYLOAD = 11
    #Configuration values
    PRINT_PDF = False
    SHOW_BITMAP_IMAGE = False
    SHOW_POISSON_GRAPH = False
    SHOW_BURST_GRAPH = False
    WRITE_TO_file = True
    PRINT_ALL = False
    #repetitions = 10
    '''Fragment error rate (probability to enter a burst) FER * 100 = % 0.01 * 100 = 1%'''
    FER = 0.02
    #Repetitions to calculate Poisson distributions
    poisson_repetitions = 10000000
    '''Burst average value '''
    poisson_lambda = 10
    
    '''Fragment error rate (Random probability) FER % -> 10 %'''
    FER_RANDOM = 20
    
    '''Save path for output files'''
    save_path = '/graphs/'

```

The out are located in graphs/ and are 4 .tex files with the graphs of the different variables analyzed.
Note that, for large bitmaps sizes, large number of repetitions and large error rates, the simulation time may 
scale exponentially.