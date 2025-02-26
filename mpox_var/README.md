# Mpox Variant Data Visualization

## [Website](https://fleurhes.github.io/PortfolioGC/mpox_var/)

## Context  
Many viruses contain different clades, which most familiarly during COVID-19, caused new waves of illness seemingly monthly. This concept of getting ill from the same virus name multiple times is something many people struggle to comprehend, which may have a link to decreasing vaccination numbers for viruses such as COVID and historically the flu.  

Utilizing public genome sequencing data on a strand of Clade 1 and Clade 2 Mpox, I seek to interactively visualize this data in a way that can aid the general public in comprehending the differences embedded in tens of thousands of lines of genome sequence, answering why it is crucial to get immunized against a virus of the same group but of a different clade.  

## Methodology  
To best create a visual aid, I utilized the NCBI genomes database and passed the sequence in FNA file format for:  
- A complete Clade 2 genome sample collected in 2018  
- A complete Clade 1 genome sample collected in 1998  

Utilizing the powerful and lightweight p5.js JavaScript library, I created a webpage that pulls directly from these FNA files to display the entire sequence of Clade 1 in rows with color-coded boxes representing genomes in a sequence, along with a button to switch clades.  

### UX Features
- Switching Clades:  
  - When a user switches clades, the rows will automatically transition to the Clade 2 sequence, showing the drastic differences in genomic sequencing between what many falsely believe to be the same.  
- Zoom Slider:  
  - A functional zoom slider allows users to decrease the number of genomes shown per row, leading to further comprehension on a smaller sample of the full sequence.  
- This sequence comparison is written to be easily interchangeable with any other sequence in the FNA format.   

## Possible Applications 
This visualization effectively represents the differences on the genomic level, aiding in the reinforcement of the impact of viruses on global health. It can aid the public in better understanding why viruses continue to impact on a global scale each year. 

 
 
