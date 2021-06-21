library(tools)
library(exams)

args = commandArgs(trailingOnly=TRUE)

assunto <- args[1]
set.seed(strtoi(args[2]))
n <- strtoi(args[3])

myexam <- dir(paste0("./CriaAtividade"), pattern = ".rnw", ignore.case=TRUE)

exams2moodle(myexam, n=n, rule="none", 
             dir="./CriaAtividade",
             edir="./CriaAtividade",
             schoice = list(shuffle = TRUE), 
             converter = "pandoc-mathjax",
             name = paste0(assunto),
             svg = TRUE,
             encoding = "UTF-8")