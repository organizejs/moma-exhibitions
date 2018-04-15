# Analysis of the Diversity of the MoMA's exhibitions

The purpose of this effort is to understand who the MoMA, as one of the leading contemporary and modern art institutions, chooses to make visible as participants of the canon of modern and contemporary art. 

### Specific goals:
- make the MoMAs archive of exhibitions, and artists who have been exhibited, available as downloadable files (.pkl)
- understand the MoMAs exhibitions and diversity of the artists who are exhibited by the MoMA
  - how many white vs non-white artists are exhibited year-over-year?
  - who are the top 100 most exhibited artists in the past 10 years, and what demographics do these artists fall into?
  - in what demographics are the artists whom the MoMA has facilitated solo exhibitions for?
  - of the nationalities that are exhibited by the MoMA, how many are white-majority nations vs non-white-majority nations?

### Downloadable pickled datasets:
One of the goals is to make the datasets accessible to other analysts to experiment with. 

#### artists
Download the pickled file from "data/artist_MMDDYYYY.pkl"

| artist_name | exhibitions | nationality | work_online | gender | race | 
| --- | --- | --- | --- | --- | --- |
| Pablo Picasso | 313 | Spanish | 1242 | male | hispanic |
| Henri Matisse | 234 | French | 366 | male | white | 
| .. | .. | .. | .. | .. | .. |

#### exhibitions
Download the pickled file from "data/exhibition_MMDDYYYY.pkl"

| year | artists | artist_count | date_full_text | exhibition_title | musuem | press_release |
| --- | --- | --- | --- | --- | --- | --- |
| 2017 | Peter Cook, Cristiano Toraldo di Francia, Gian... | 17 | November 15, 2006–March 26, 2007 | OMA in Beijing: China Central Television Headq... | The Museum of Modern Art | <p>This exhibition presents one of the most in... | 
| 2007 | Brice Marden | 1 | October 29, 2006–January 15, 2007 | Brice Marden: A Retrospective of Paintings and... | The Museum of Modern Art | <p>This exhibition presents one of the most in... | 
| .. | .. | .. | .. | .. | .. | .. |

# Data Collection [Methodology]:
The outline of the steps that are taken to acquire the data.
1. Scrape exhibition and artist data from the MoMA's website
2. Assign race to each artist
3. Assign gender to each artist

Please see the data-collection.ipynb to view the code.

## Web scraping
As of 4/6/18, the MoMA has had 4968 exhibits.

The exhibition dataset is a set of all exhibitions that have been hosted by the The Museum of Modern Art, MoMA PS1, or moma.org. Exhibitions can be scraped from urls such as: [https://www.moma.org/calendar/exhibitions/100](https://www.moma.org/calendar/exhibitions/100), where 100 represents the id of some exhibit.

The artist dataset is created by compiling all artists across all exhibits and removing any duplication. This set of artists will be different from the dataset of artists in their [collection](https://www.moma.org/collection/) since the MoMA does not have to collect an artist's work in order to have shown them. For each exhibit, i, we scrape data from a url : https://www.moma.org/artists?exhibition_id=i

## Identifying Race & Gender
When it comes to trying to understand the diversity of the artists that have been exhibited by the MoMA, I've chosen to look at race and gender (as opposed to other dimensions such as sexual orientation, ability, etc) because I am able to produce a prediction on race and gender to some degree of accuracy based on the available information (specifically on artist name and nationality).

### Race Data
To get an artist's race, I use a two fold method:

#### Part One:

First I use the python library: [__ethnicolr__](https://github.com/appeler/ethnicolr), that matches names to race. This python library provides several bi-char (Smith ==> sm, mi, it, th) deep learning models that use an LSTM architecture. The specific model I chose is based on wikipedia data as it uses the most international dataset to train the model. It has a model performance of 80% accuracy and 83% recall.

#### Part Two:

For the second part, I try to increase the accuraccy specifically on American artists using the data from the [US-Census](https://api.census.gov/data/2010/surname.html).

To take a conservative stance, I only reassign artists whose race is predicted to be 'white' from _ethnicolr_. If _ethnicolr_ predicts a non-white race, I keep the race assignment as is. This means that I will end up with an under-estimation of white artists, and an over estimation of non-white artists. 

The first part is to figure out what part of the artist_name string is the lastname. To do this, I start from the last word of the artist_name, and iteratively check whether or not the word has a match in the lastname_race_df.

For example, if we get the name "Millie Bobby Brown", 
1. I will start by checking whether or not 'Brown' maps to some name in the lastname_race_df 
2. if so, I will assign the artist with a race, otherwise, check to see whether or not 'Bobby' maps to some name in the lastname_race_df
3. if so, I will assign the artist with a race, otherwise, check to see whether or not 'Millie' maps to some name in the lastname_race_df
4. if so, I will assign the artist with a race, otherwise, we keep the race prediction of _ethnicolr_

The race assignment is done by randomly sampling from probabilities provided in the US Census dataset. This will mean that on each run, there is a chance that the race assigned to each artist will be different.

For example, if we were to assign the lastname "Brown" to a race, we will start by looking for the probability distribution of races. We then randomly sample from this distribution to get our prediction:

### Gender Data
To get an artist's gender, I used the web service: [__genderize.io__](https://www.genderize.io). This service simply takes in a name and spits out a gender, and the probability of its accuracy. 

## Data Accuracy
Based off a sample of about 1400 artists, where I manual checked all artists from 1957, 1977, 1997, and 2017, the race predictions stand at ~95% accuracy while the gender predictions stand at ~99% accuracy. 

In the case of race predictions, I took a conservative approach, meaning that for every one artists who was non-white that was predicted to be white, there were many more artists who were white that was predicted to be non-white.

## Limitations of this methodology:
When producing these dataset, it was put into the position of identifying the race and gender categories to classify each artist by.

Because of the methodology, tools and datasets that I used, one of the primary limitations is that we are left with a binary definition of gender, limited either to male or female. This does not work for artists who do not conform to the male/female gender binary, and for artist groups that have multiple members of which there could be multiple genders.

Additionally, the races are artists are classified into either white, black, asian, hispanic, indian or aian (Native Hawaiian or Other Pacific). As race is a social construct, this classification is somewhat arbitrary, and there are often cases where people do not identify with any one of these categories. 
