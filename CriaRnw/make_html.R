library(tools)
library(exams)

args = commandArgs(trailingOnly=TRUE)

set.seed(strtoi(args[2]))

exams2html(list(args[1]), n=1, solution=TRUE, mathjax=TRUE,
           encoding = "UTF-8",
           dir = './html',
           edir = ".",
           template = "plain.html")
