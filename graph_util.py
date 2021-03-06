import re
import sys

def parserFile(filename):
    readnumber = re.compile('[r]+\d+')
    line_spliter = re.compile('\t+')
    colon_spliter = re.compile(':')
    forward_reads = 0
    reverse_reads = 0
    unmatched_reads = 0
    read_quality = [[]]
    match_scores = []
    f = open(filename)
    lines = f.readlines()
    for i in range(3, len(lines)):
        get_match_score = True
        subline = line_spliter.split(lines[i])

        if (subline[1] == '0'):
            forward_reads += 1
        elif (subline[1] =='16'):
            reverse_reads += 1
        else:
            unmatched_reads += 1
            get_match_score = False

        for j in range(len(subline[10])):
            while(len(read_quality) < len(subline[10])):
                read_quality.append([])
            read_quality[j].append(subline[10][j])

        if (get_match_score):
            match_scores.append(int(colon_spliter.split(subline[11])[2]))
    read_quality = read_quality_converter(read_quality)
    return (forward_reads, reverse_reads, unmatched_reads, read_quality, match_scores)


def matched_vs_unmatched_pie_chart(forward_reads, reverse_reads, unmatched_reads):
    match_chart_labels = ['Forward Reads(Matched)', 'Reverse Reads (Matched)', 'Unmatched Reads']
    match_chart_values = [forward_reads, reverse_reads, unmatched_reads]
    return (match_chart_labels, match_chart_values)

def phred33_to_q(qual):
  return ord(qual)-33

def read_quality_converter(read_quality):
    for i in range(len(read_quality)):
        for j in range(len(read_quality[i])):
            read_quality[i][j] = phred33_to_q(read_quality[i][j])
    return read_quality

def make_data_for_box_plot(read_quality):
    data = [[]]
    for i in range(len(read_quality)):
        data.append(read_quality[i])
    return data

def parseString(txt):
    spliter = re.compile('\n+')
    readnumber = re.compile('[r]+\d+')
    line_spliter = re.compile('\t+')
    colon_spliter = re.compile(':')
    forward_reads = 0
    reverse_reads = 0
    unmatched_reads = 0
    tlen = []
    read_quality_unpaired = [[]]
    read_quality_first = [[]]
    read_quality_second = [[]]
    match_scores = []
    mapq_scores = []

    lines = spliter.split(txt)
    #Itterating though everyline
    for i in range(len(lines) - 1):
        get_match_score = True
        subline = line_spliter.split(lines[i])
        if (int(subline[1]) & 4 == 4):
            unmatched_reads += 1
            get_match_score = False
        elif (int(subline[1]) & 16 == 16):
            reverse_reads += 1
        else:
            forward_reads += 1
        if(int(subline[1]) & 2 == 2): #read is paired
            tlen.append(abs(int(subline[8])))
            if(int(subline[1]) & 64 == 64):
              for j in range(len(subline[10]) - 1):
                  while(len(read_quality_first) < len(subline[10])):
                      read_quality_first.append([])
                  read_quality_first[j].append(subline[10][j])
            elif(int(subline[1]) & 128 == 128):
              for j in range(len(subline[10]) - 1):
                  while(len(read_quality_second) < len(subline[10])):
                      read_quality_second.append([])
                  read_quality_second[j].append(subline[10][j])
        else: #read is unpaired
          for j in range(len(subline[10]) - 1):
              while(len(read_quality_unpaired) < len(subline[10])):
                  read_quality_unpaired.append([])
              read_quality_unpaired[j].append(subline[10][j])

        if (get_match_score):
            match_scores.append(int(colon_spliter.split(subline[11])[2]))
            mapq_scores.append(int(subline[4]))
    read_quality_unpaired = read_quality_converter(read_quality_unpaired)
    read_quality_first = read_quality_converter(read_quality_first)
    read_quality_second = read_quality_converter(read_quality_second)
    return (forward_reads, reverse_reads, unmatched_reads, read_quality_unpaired, read_quality_first, read_quality_second, match_scores, tlen, mapq_scores)

def parseAlignmentSummary(txt):
    sys.stderr.write(txt)
    spliter = re.compile('\n+')
    line_spliter = re.compile('\s+')
    summary_finder = re.compile('\d+\sreads;\sof\sthese:')
    sys.stderr.write(summary_finder.split(txt)[-1])
    if summary_finder.search(txt):
        txt = summary_finder.split(txt)[-1]
    lines = spliter.split(txt)
    unaligned = int(line_spliter.split(lines[2])[1])
    aligned = int(line_spliter.split(lines[3])[1])
    multi_aligned = int(line_spliter.split(lines[4])[1])
    return (unaligned, aligned, multi_aligned)


def matched_vs_unmatched_pie_chart(forward_reads, reverse_reads, unmatched_reads):
    match_chart_labels = ['Forward Reads(Matched)', 'Reverse Reads (Matched)', 'Unmatched Reads']
    match_chart_values = [forward_reads, reverse_reads, unmatched_reads]
    return (match_chart_labels, match_chart_values)

def phred33_to_q(qual):
  #Turn Phred+33 ASCII-encoded quality into Phred-scaled integer
  return ord(qual)-33

def read_quality_converter(read_quality):
    for i in range(len(read_quality)):
        for j in range(len(read_quality[i])):
            #Converting the read quality data to probabilities
            read_quality[i][j] = phred33_to_q(read_quality[i][j])
    return read_quality

def make_data_for_box_plot(read_quality):
    data = [[]]
    for i in range(len(read_quality)):
        data.append(read_quality[i])
    return data
