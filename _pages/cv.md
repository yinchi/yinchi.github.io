---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
---------

* Ph.D, City University of Hong Kong, 2017
  * **Thesis Title**: Surrogate-based Approximation of Blocking Probability in Non-hierarchical Overflow Loss Systems
  * **Supervisor**: [Dr. Eric W. M. Wong](http://www.ee.cityu.edu.hk/~ewong/)
  * Co-supervisor: [Prof. Moshe Zukerman](http://www.ee.cityu.edu.hk/~zukerman/)
* M.Sc. in Multimedia Information Technology, City University of Hong Kong, 2011
* B.Math., University of Waterloo, 2010

Work experience
---------------

### Research Associate (Dec. 2021-present)
  * Institute for Manufacturing, University of Cambridge
  * **Supervisor**: Prof. Ajith Parlikad
  * Developed discrete-event simulation models and web dashboards for predicting hospital bed occupancy of COVID-19 patients, for capacity planning and to support recovery of selected non-Covid services.
  * **Current activities**:
    * Develop discrete-event simulation models and web dashboards for process modelling in a histopathology lab, for KPI prediction, resource planning, and process optimisation.
    * Set the foundation for developing hospital digital twins, deepening understanding of hospital operations, asset management, and patient outcomes.

### Research Associate (2020-2021), Research Fellow (2018-2020), Postdoctoral Fellow (2016-2018)
  * City University of Hong Kong
  * **Supervisor**: Dr. Eric W. M. Wong
  * Assisted in the writing of grant applications and project reports, especially in the area of healthcare operations management.
  * Developed analytical and simulation models for the evaluation, and optimization of intensive care networks in Hong Kong and other metropolitan cities.
  * Developed stochastic models for infectious disease.
  * Developed simulation and analytical approximation methods for blocking probability in overflow loss system models, including machine learning-based methods, with applications in various telecommunications and service systems.
  * Mentored undergraduate students on the completion of their final year projects.
  * Instructed final-year undergraduate students on writing simulation programs for stochastic system models.

### Co-lecturer, University of the Witwatersrand, South Africa (Jul-Sep 2021)
  * Co-lecturer of the capstone course “Design Project” on engineering design for students in Electrical and Information Engineering.
  * I was invited to co-lecture this course thanks to my previous collaboration with Prof. Anton van Wyk on epidemiological modelling for COVID-19.
  * Students choosing our selected topic would need to design a simple epidemiological model for COVID-19, analyze possible tipping points leading to an out-of-control local epidemic, and design an early-warning system to avoid hitting these tipping points.
  
Skills
------

* Extensive experience with discrete-event simulation in Python (using the [SimPy](https://simpy.readthedocs.io/en/latest/index.html) and [salabim](https://www.salabim.org/) libraries)
* Markov-chain simulation
* Web app development using Flask and [Python Dash](https://dash.plotly.com/)
* Some experience in R, MATLAB, Julia, Java, C++, and SQL.
* Some experience with Docker and Docker Compose
* Document preparation with LaTeX and R [bookdown](https://bookdown.org/)

Publications
------------
  <ol>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ol>

### Preprints

  <ol>{% for post in site.preprints reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ol>
  
Talks
-----
  <ol>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html %}
  {% endfor %}</ol>

Patent
------

1. W. M. E. Wong, J. T. Wu, **Y. C. Chan**, and M. Zukerman, “Base station
sleep mode based on power consumption and/or quality of service,” US
patent [US10568047B2](https://patents.google.com/patent/US10568047B2/en), City University of Hong Kong, 18 Feb. 2020. (Filed 12 Jan. 2018)
[PDF](/files/patent_047.pdf)

## Continuing education

**Data Science** (HarvardX)
  * Course provider: edX
  * Nine courses on data science using the R tidyverse packages, including plotting, inference and modelling, data wrangling, and string processing.
  * [Program record](https://credentials.edx.org/records/programs/shared/dceaa9b46cfb41ac82204d9c8abeaa0d)

**Epidemics - Origins, Spread, Control and Communication** (HKUx)
  * Course provider: edX
  * Four courses on the origins, spread and control of infectious disease epidemics and eﬀective communication about infectious diseases
  * [Program record](https://credentials.edx.org/records/programs/shared/844bacdaae2f4a51a0b1f835c3b650b9)
  