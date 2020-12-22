### Supervised Learning Models for
### Analysis of Impactful Program Components

## Classification: Linear Classifiers, Support Vector Machines, Decision Trees, K-Nearest Neighbor, Random Forest
## Regression: Linear Regression (GPA), Logistic Regression (Graduated?)

## Clear workspace
rm(list=ls())
dev.off()

## Import dataset
full <- read.csv("Cohort Dataset.csv", header = TRUE, sep = ",")
myvars <- c("RPRAWRD_FUND_CODE", "FIRST.GENERATION", "Count.Special", "Faculty.Mentor", "Peer.Mentor", 
            "Scholarship.Stipend", "Research", "Student.Enrichment", "In.Cohort.", "Mentorship", "Spel.Grad.",
            "GPA", "Yrs.Enrolled")
data <- full[myvars]


### Convert to categorical
data$RPRAWRD_FUND_CODE = as.factor(data$RPRAWRD_FUND_CODE)
data$FIRST.GENERATION = as.factor(data$FIRST.GENERATION)
data$In.Cohort. = as.factor(data$In.Cohort.)
data$Spel.Grad. = as.factor(data$Spel.Grad.)

data2 <- subset(data, Spel.Grad. == "True")

## Split data into train and test
### 75% of the sample size
smp_size <- floor(0.75 * nrow(data))
smp_size2 <- floor(0.75 * nrow(data2))  ## all graduates

## set the seed to make your partition reproducible
set.seed(123)
train_ind <- sample(seq_len(nrow(data)), size = smp_size)
train_ind2 <- sample(seq_len(nrow(data2)), size = smp_size2)

train <- data[train_ind, ]
train2 <- data[train_ind2, ]
test <- data[-train_ind, ]
test2 <- data[-train_ind2, ]

data.cor = cor(data[sapply(data, function(x) !is.factor(x))])

#install.packages("corrgram")
library(corrgram)
palette = colorRampPalette(c("green", "white", "red")) (20)
heatmap(x = data.cor, col = palette, symm = TRUE)

corrgram(data, order=TRUE, lower.panel=panel.shade,
         upper.panel=panel.pie, text.panel=panel.txt,
         main="Car Milage Data in PC2/PC1 Order")

install.packages("corrplot")
library(corrplot)
corrplot(data.cor, method="number")

### Basic Decision Tree Model ###
#install.packages("tree")
library(tree)

tree.model1 <- tree(Spel.Grad. ~ RPRAWRD_FUND_CODE + FIRST.GENERATION + In.Cohort. + Count.Special + Faculty.Mentor
                    + Peer.Mentor + Scholarship.Stipend + Research + Student.Enrichment + GPA + Yrs.Enrolled, train)
plot(tree.model1)
text(tree.model1,pretty =0, cex=0.8)
title("Decision Tree | 2013-2016 Cohorts")

tree.model2 <- tree(Spel.Grad. ~ RPRAWRD_FUND_CODE + FIRST.GENERATION + In.Cohort. + Count.Special + Faculty.Mentor
                    + Peer.Mentor + Scholarship.Stipend + Research + Student.Enrichment + GPA + Yrs.Enrolled, train2)
summary(tree.model2)
plot(tree.model2)
text(tree.model2,pretty =0, cex=0.8)
title("Decision Tree | 2013-2016 Cohorts (Spel.Grad.=='Y')")

## Check model accuracy
t_pred = predict(tree.model1,test,type="class")
confMat <- table(test$Spel.Grad.,t_pred)
accuracy <- sum(diag(confMat))/sum(confMat)
accuracy

t_pred2 = predict(tree.model2,test2,type="class")
confMat2 <- table(test2$Spel.Grad.,t_pred2)
accuracy2 <- sum(diag(confMat2))/sum(confMat2)
accuracy2

##############################################################################################
### Tree Pruning ###
install.packages("rpart")
library(rpart)
fit <- rpart(Spel.Grad. ~ RPRAWRD_FUND_CODE + FIRST.GENERATION + In.Cohort. + Count.Special + Faculty.Mentor
             + Peer.Mentor + Scholarship.Stipend + Research + Student.Enrichment + GPA + Yrs.Enrolled, method = "class", data = train)

printcp(fit) # display the results 
plotcp(fit) # visualize cross-validation results 
summary(fit) # detailed summary of splits

# plot tree 
plot(fit, uniform=TRUE, main="Classification Tree for Kyphosis")
text(fit, use.n=TRUE, all=TRUE, cex=.8)


install.packages("rpart.plot")
library(rpart.plot)
rpart.plot(fit)
print(fit)

### Pruning?
ptree = prune.rpart(fit, fit$cptable[which.min(fit$ptable[,"xerror"]),"CP"])
rpart.plot(ptree)

## Model Performance:
cv.DT =cv.tree(tree.model1)
plot(cv.DT$size,cv.DT$dev,type='b', col="blue")
best.tree.size <- cv.DT$size[which.min(cv.DT$dev)]
best.tree.size

#prune.rpart()
prune.DT = prune.tree(tree.model1,best = best.tree.size)
plot(prune.DT)
text(prune.DT,pretty =0)

#### Predict response

pred <- predict(fit, test, type="class")
#table(predict(fit, iris[-sub,], type = "class"), iris[-sub, "Species"])
length(pred)
length(test)
T <- table(pred, test$Spel.Grad.)
T

install.packages("caret")
library(caret)
#confusionMatrix(pred, test$Spel.Grad.)
t_pred3 = predict(tree.model1,test,type="class")
confMat3 <- table(test$Spel.Grad.,t_pred3)
accuracy <- sum(diag(confMat3))/sum(confMat3)
accuracy
