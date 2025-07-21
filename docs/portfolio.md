# Portfolio

## [Code for paper "Data integration for space-aware Digital Twins of hospital operations"](https://github.com/yinchi/histopath-bim-des)

This code accompanies the Automation in Construction paper "[Data integration for space-aware Digital Twins of hospital operations](https://www.sciencedirect.com/science/article/pii/S0926580525003164)".  It simulates the handling of specimens in a histopathology laboratory, and examines the effect of building layout and infrastructure status on the lab turnaround time.  The [`salabim`](https://www.salabim.org/manual/Overview.html) Python library is used for discrete-event simulation.

## [HarvardX PH125.9x: Movielens Project](https://yinchi.github.io/harvardx-movielens/)

R project for partial completion of the edX course HarvardX PH125.9x: “Data Science: Capstone”.

The objective of this project was to build a movie recommendation system using the [MovieLens](https://grouplens.org/datasets/movielens/10m/) dataset. The final model presented uses linear regression with matrix factorisation on the residuals, and acheives a root mean squared error of 0.782 when estimating the ratings (out of 5) of movies in the test set.

To accelerate the matrix factorisation portion, RCpp was used [along with the Armadillo](https://dirk.eddelbuettel.com/code/rcpp.armadillo.html) C++ library.

## [HarvardX PH125.9x: Higgs dataset classification](https://yinchi.github.io/harvardx-higgs/)

R project for partial completion of the edX course HarvardX PH125.9x: “Data Science: Capstone”.

In this project, neural networks (via [Keras in R](https://keras3.posit.co/)) was used to predict particle collision events using the HIGGS dataset. The final NN was generated with three hidden layers of 2048 nodes each, generating a final area under the ROC curve (AUC) of 0.877. It was found that using high-level (derived) features provided only a small improvement in AUC, compared to using low-level features only.

## [SimPy Examples](https://github.com/yinchi/simpy-examples/)

These short examples were created to teach discrete-event simulation to Electrical Engineering final-year project students at the City University of Hong Kong. The SimPy Python library was used for this purpose. SimPy is based on the use of Python generators and a Environment object that is shared between components of the simulation.
