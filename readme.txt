Assumptions

Log File Format:

This program supports only default format of flow log records (i.e records with only version 2 fields as mentioned in AWS userguide)



Lookup Table Format:

The problem description contained an inconsistency regarding the lookup table format:

In the Requirements section, it specified the lookup table as a .txt file.
At the start of the Problem Description, it referred it as a .csv file.
To address this ambiguity, I provided a flexible solution as I implemented support for both file types (.txt and .csv). 

Here’s how it works:
.txt files: Treated as plain ASCII text files, with each line representing a record with no header. Columns should be separated by commas.
.csv files: Processed using a CSV parser to handle standard CSV formatting, first line will be always read as a header.


Protocol mapping:

This program uses standard protocol numbers for mapping the numeric protocol identifier found in log records to its corresponding protocol type. 
This mapping is based on the widely recognized IANA (Internet Assigned Numbers Authority) protocol numbers like
    6: tcp 
    1: icmp 
    17: udp

If the numeric protocol from the log record does not match any known standard protocols, it will be classified as unknown in the output.



Analysis:

First, load the lookup table in map for quick lookups as it would cost O(1) time for every record by checking (dstport,protocol) from log
Then, while reading every recod from the input log file updating the corresponding maps for storing counts of tag and port/protocol respectively

total time complexity is O(M+N) 
time to build lookup table map - O(M)
time to process and update results for each record is O(1), for N records O(N)

Space complexity is O(M+N)
storing M records from lookup table in map - O(M)
storing results of N records from log file in map - O(N)


Instructions to Run:
Execute process.py file and make sure input files are named accordingly.


Tests:

Tested using sample log files from online and performed manual tests on edge cases. 
Verified compatibility with both .txt and .csv lookup tables, ensuring correct tag mappings across different formats.