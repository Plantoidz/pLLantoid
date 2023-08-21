#!/bin/bash

inputfile="$1"
prefix="chunk_"
duration=59

# Get the duration of the video in seconds
total_duration=$(ffmpeg -i "$inputfile" 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | awk '{ split($1, A, ":"); print 3600*A[1] + 60*A[2] + A[3] }')

# Calculate number of chunks
num_chunks=$(echo "$total_duration / $duration" | bc)

# Split the video
for (( i=0; i<=$num_chunks; i++ ))
do
    start_time=$(echo "$i * $duration" | bc)
    ffmpeg -i "$inputfile" -ss "$start_time" -t "$duration" -c copy "${prefix}${i}.mp3"
done
