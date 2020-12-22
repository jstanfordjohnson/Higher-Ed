### Exploratory Analysis for
### Analysis of Impactful Program Components

## Clear workspace
rm(list=ls())
dev.off()

## Import dataset
data <- read.csv("Cohort Dataset.csv", header = TRUE, sep = ",")
data2 <- subset(data, Spel.Grad. == "True")
dim(data)[1]

## Create subdataset with numeric factors
myvars <- c("Faculty.Mentor", "Peer.Mentor", "Scholarship.Stipend", "Research", "Student.Enrichment", "Yrs.Enrolled", "GPA")
newdata <- data[myvars]
newdata2 <- data2[myvars]

# Correlation matrix #
library(corrplot)
mydata.cor = cor(newdata)
#corrplot(mydata.cor)
corrplot(mydata.cor, method="number")

# Ranked Cross-Correlation #
library('lares')
corr_cross(newdata, max_pvalue = 0.05, top = 10)
corr_cross(newdata2, max_pvalue = 0.05, top = 10)

## JSJ: Based on the ranked cross-correlations, create additional program components categories?
## e.g., scholarship only, staff leadership

# Scatterplots of Highly Correlated Factors
library(ggplot2)
fr <- ggplot(data, aes(Faculty.Mentor, Research, colour = Spel.Grad.)) + geom_point() 
fm <- ggplot(data, aes(Faculty.Mentor, Student.Enrichment, colour = Spel.Grad.)) + geom_point()
fs <- ggplot(data, aes(Faculty.Mentor, Scholarship.Stipend, colour = Spel.Grad.)) + geom_point() 

ggplot(data2, aes(Faculty.Mentor, Research, size = factor(nrow))) + geom_point() + scale_size_discrete(range = c(3, 7))

ggplot(data2, aes(Faculty.Mentor, Research, size = factor(nrow))) + geom_point() + scale_size_discrete(range = c(3, 7))
fm2 <- ggplot(data2, aes(Faculty.Mentor, Student.Enrichment, colour = Spel.Grad.)) + geom_point()
fs2 <- ggplot(data2, aes(Faculty.Mentor, Scholarship.Stipend, colour = Spel.Grad.)) + geom_point() 

ggplot(data2, aes(Faculty.Mentor, Research, colour = c("green", "blue", "orange", "red"))) + geom_point() 

ggplot(data, aes(GPA, Research, size = Faculty.Mentor, color = Spel.Grad.)) + geom_point(alpha=0.5) + 
    scale_size_continuous(range = c(.1, 6))


ggplot(mydf, aes(x = x, y = y)) + 
  geom_point(aes(size = count)) +
  scale_size_continuous(range = c(3, 7))

#install.packages("cowplot")
library(cowplot)

plot_grid(fr, fm, fs, labels = "AUTO")
plot_grid(fr2, fm2, fs2, labels = "AUTO")

#ggplot(data, aes(fill=Spel.Grad., y=GPA, x=Yrs.Enrolled)) + 
#  geom_bar(position="dodge", stat="identity")

ggplot(data, aes(Yrs.Enrolled, ..count..,,fill=Spel.Grad.)) + 
  geom_bar(aes(fill = Spel.Grad.), position = "dodge")+
  geom_text(aes(label=..count..),stat='count',position=position_dodge(0.9))+
  theme_minimal()+
  scale_fill_brewer(palette="Paired")+
  labs(x="Years Enrolled",y="Count")
