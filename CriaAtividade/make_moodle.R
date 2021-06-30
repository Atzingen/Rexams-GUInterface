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