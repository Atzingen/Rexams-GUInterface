if(!require(exams)){
    install.packages("exams", dependencies = TRUE, repos='http://cran.us.r-project.org')
    library(exams)
}

if(!require(tools)){
    install.packages("tools", repos='http://cran.us.r-project.org')
    library(tools)
}

library(tools)
library(exams)

args = commandArgs(trailingOnly=TRUE)

set.seed(strtoi(args[2]))

exams2html(list(args[1]), n=1, solution=TRUE, mathjax=TRUE,
           encoding = "UTF-8",
           dir = './html',
           edir = ".",
           template = "plain.html")
