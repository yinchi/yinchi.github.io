---
title: "Projects"
description: "Full list of Yin-Chi Chan's software, data science, and academic projects."
type: page
---

## Command-line LLM chatbot demo

<https://github.com/yinchi/openai_demo>

This simple chatbot uses the OpenAI [Chat Completions API](https://developers.openai.com/api/reference/python/resources/chat/subresources/completions)
to generate responses to user input. Responses are interpreted as Markdown and rendered in the
terminal using the [rich](https://github.com/Textualize/rich) Python library. Available tools
include file read/write, Python code execution, and web search via the
[Brave Search API](https://brave.com/search/api/).

The chatbot was tested locally using a [vLLM](https://vllm.ai) instance running the
[`google/gemma-4-26B-A4B-it`](https://huggingface.co/google/gemma-4-26B-A4B-it) model. A
`gemma.sh` script is included in the repo to simplify the process of launching the vLLM
instance with the correct parameters.

{{< img src="/images/projects/openai_demo.png" title="OpenAI demo screenshot" >}}

## CodeCrafters

<https://app.codecrafters.io/users/yinchi>

CodeCrafters is a website filled with coding challenges involving recreating simplified
versions of common software such as an HTTP server, a terminal shell, a programming language
interpreter, and a CLI LLM tool. The profile page above tracks my progress through various
challenges offered by the website.

Published challenge solutions:

- [Rust: interpreter](https://github.com/yinchi/codecrafters-interpreter-rust) &mdash; follows
  Part II of the book [Crafting Interpreters](https://craftinginterpreters.com/contents.html) by
  Robert Nystrom, building a tree-walk interpreter for the Lox programming language. Features
  include a finite-state-machine tokenizer, a recursive-descent parser, and a resolver for
  handling variable scopes. The language is a simple dynamically-typed language with
  Python-like syntax, functions, classes, and inheritance.
- [Rust: HTTP Server](https://github.com/yinchi/codecrafters-http-server-rust) &mdash; a simple
  HTTP/1.1 static file server that can handle multiple concurrent, persistent connections.
- [Python: CLI LLM tool](https://github.com/yinchi/codecrafters-claude-code-python) &mdash; this
  challenge is still in beta on the CodeCrafters website but uses the OpenAI API to communicate
  with an LLM. A small set of available tools are advertised. As a permissions system was not
  implemented as part of this challenge (it has been proposed as a
  [future extension](https://app.codecrafters.io/roadmap/challenge-extensions?course=claude-code)),
  I stuffed my local test environment inside a Docker container for isolation.

## Other projects

### [Ring puzzle](https://yinchi.github.io/ring_puzzle/)

Clone of the classic Top Spin puzzle by Binary Arts. Auto-solver included based on a greedy
algorithm plus endgame table lookup. Full blog post
[here](https://yinchi.github.io/blog/2026/05/15/top-spin/).

### [&mu;py](https://github.com/yinchi/upy/)

MicroPython in a Docker container, all under 10MB!

I made this because the current pre-built `micropython/unix` Docker image on
[Docker Hub](https://hub.docker.com/r/micropython/unix) is hardly smaller than a typical
`python` image. One can use my Docker image to test an MQTT IoT network setup with a large
number of virtual sensors; the example script included in the repo can be used for this.

The included `Dockerfile` sets up MicroPython and also installs a small set of MicroPython
packages (required by the example script).

### [Code for paper "Data integration for space-aware Digital Twins of hospital operations"](https://github.com/yinchi/histopath-bim-des)

This code accompanies the Automation in Construction paper
"[Data integration for space-aware Digital Twins of hospital operations](https://www.sciencedirect.com/science/article/pii/S0926580525003164)".
It simulates the handling of specimens in a histopathology laboratory, and examines the effect
of building layout and infrastructure status on the lab turnaround time. The
[`salabim`](https://www.salabim.org/manual/Overview.html) Python library is used for
discrete-event simulation.

### [HarvardX PH125.9x: Movielens Project](https://yinchi.github.io/harvardx-movielens/)

R project for partial completion of the edX course HarvardX PH125.9x: "Data Science:
Capstone".

The objective of this project was to build a movie recommendation system using the
[MovieLens](https://grouplens.org/datasets/movielens/10m/) dataset. The final model presented
uses linear regression with matrix factorisation on the residuals, and achieves a root mean
squared error of 0.782 when estimating the ratings (out of 5) of movies in the test set.

To accelerate the matrix factorisation portion, I used Rcpp
[along with the Armadillo](https://dirk.eddelbuettel.com/code/rcpp.armadillo.html) C++ library
to implement [Simon Funk's matrix factorisation algorithm](https://sifter.org/simon/journal/20061211.html).

### [HarvardX PH125.9x: Higgs dataset classification](https://yinchi.github.io/harvardx-higgs/)

R project for partial completion of the edX course HarvardX PH125.9x: "Data Science:
Capstone".

In this project, neural networks (via [Keras in R](https://keras3.posit.co/)) were used to
predict particle collision events using the HIGGS dataset. The final NN was generated with
three hidden layers of 2048 nodes each, generating a final area under the ROC curve (AUC) of
0.877. It was found that using high-level (derived) features provided only a small improvement
in AUC, compared to using low-level features only.

### [SimPy Examples](https://github.com/yinchi/simpy-examples/)

These short examples were created to teach discrete-event simulation to Electrical Engineering
final-year project students at the City University of Hong Kong. The SimPy Python library was
used for this purpose. SimPy is based on the use of Python generators and an Environment object
that is shared between components of the simulation.
