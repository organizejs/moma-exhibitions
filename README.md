# Analysis of the Diversity of the MoMA's exhibitions

The purpose of this effort is to understand who the MoMA, as one of the leading contemporary and modern art institions, chooses to make visible as participants of the canon of modern and contemporary art. 

### Specific goals:
- make the MoMAs archive of exhibitions, and artists who have been exhibited, available as downloadable files (.pkl)
- understand the MoMAs exhibitions and diversity of the artists who are exhibited by the MoMA
  - how many white vs non-white artists are exhibited year-over-year?
  - who are the top 100 most exhibited artists in the past 10 years, and what demographics do these artists fall into?
  - in what demographics are the artists whom the MoMA has facilitated solo exhibitions for?

### Downloadable pickled datasets:
One of the goals is to make the datasets accessible to other analysts to experiment with. 

__artists__
Download the pickled file from "data/artist_MMDDYYYY.pkl"

| artist_name | exhibitions | nationality | work_online | gender | race | 
| --- | --- | --- | --- | --- | --- |
| Pablo Picasso | 313 | Spanish | 1242 | male | hispanic |
| Henri Matisse | 234 | French | 366 | male | white | 
| .. | .. | .. | .. | .. | .. |

__exhibitions__
Download the pickled file from "data/exhibition_MMDDYYYY.pkl"

| year | artists | artist_count | date_full_text | exhibition_title | musuem | press_release |
| --- | --- | --- | --- | --- | --- | --- |
| 2017 | Peter Cook, Cristiano Toraldo di Francia, Gian... | 17 | November 15, 2006–March 26, 2007 | OMA in Beijing: China Central Television Headq... | The Museum of Modern Art | <p>This exhibition presents one of the most in... | 
| 2007 | Brice Marden | 1 | October 29, 2006–January 15, 2007 | Brice Marden: A Retrospective of Paintings and... | The Museum of Modern Art | <p>This exhibition presents one of the most in... | 
| .. | .. | .. | .. | .. | .. | .. |


## Race & Gender

### Data Accuracy
Based off a sample of about 1400 artists, where I manual checked all artists from 1957, 1977, 1997, and 2017, the race predictions stand at ~95% accuracy while the gender predictions stand at ~99% accuracy. 

In the case of race predictions, I took a conservative approach, meaning that for every one artists who was non-white that was predicted to be white, there were many more artists who were white that was predicted to be non-white.
