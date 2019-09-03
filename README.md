# Data36-Junior-Data-Science-course-solution
My solution to the "Junior Data Scientist's First Month" course final project, run by data36.com. 


DESCRITPION:

The task was to produce a report for a fictional travel blog, in which the business funnel was as follows:

- New readers visit the blog.
- They read articles.
- They subscribe to the newsletter.
- They purchase info products.

The aim was to instruct the fictional blog owner as to how to spend his advertising budget, using a variety of basic data science techniques: segmentation, funnels, cohort anaylsis etc.


Contained in this repository are my solutions to these basic tasks, implemented in Python using the Pandas, Numpy, and Seaborn.


PACKAGE MANAGEMENT:

Pandas (https://pandas.pydata.org/)
Numpy (https://numpy.org/)
Seaborn (https://seaborn.pydata.org/)

REPOSITORY CONTENTS:

CSV  -  folder containing the CSV files of logged events from the fictional travel blog

        - D_firstreads.csv  # log of each user's first article read on the site. Contains additional info such as country of origin.
        - D_latereads.csv   # log of users' subsequent article reads on the site.
        - D_subs.csv        # log of user subscription events
        - D_buy.csv         # log of users' purchases on the site

Tim_Howe_final_project_presentation.pdf  - the presentation I submitted to the course organiser.

cohort_analysis.py  - an example cohort analysis, dividing users into cohorts by week of first visit.




