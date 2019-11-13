rm(list=ls())

dev.off()

#data = read.csv("research_spelman4.csv", header = TRUE)
data = read.csv("research_spelman5.csv", header = TRUE)
#data = read.csv("research_spelman6.csv", header = TRUE) ## has 2014-2017 removed
colnames(data)

##############################################################################
# Visualize the data
### Detect missing values
#install.packages("Amelia")
library(Amelia)
missmap(data, main = "Missing values vs observed")

### Plot the pairs
pairs(data, col=data$Doctorate.)

### Boxplots
install.packages("ggplot")
library(ggplot2)
ggplot(data=data, aes(x=highest.adv.tier, y=Doctorate.)) + geom_bar(stat="identity")

ggplot(data, aes(x=highest.adv.tier, y=Doctorate.)) + geom_boxplot()

### Mosaic Plot
install.packages("vcd")
library(vcd)
mosaic(Doctorate. ~ RISE., data=data, shade=TRUE, legend=TRUE)

##############################################################################
### Convert to numeric
data$num_RD = as.numeric(as.character(data$num_RD))
data$num_yrs_enrolled = as.numeric(as.character(data$num_yrs_enrolled))


### Convert to categorical
data$same.advisor. = as.factor(data$same.advisor.)
data$highest.adv.tier = as.factor(data$highest.adv.tier)
data$Honors. = as.factor(data$Honors.)
data$RISE. = as.factor(data$RISE.)
data$Doctorate. = as.factor(data$Doctorate.)
data$Cohort = as.factor(data$Cohort)
data$Class = as.factor(data$Class)
data$Graduated. = as.factor(data$Graduated.)
data$same.topic. = as.factor(data$same.topic.)

## Split data into train and test
### 75% of the sample size
smp_size <- floor(0.75 * nrow(data))

## set the seed to make your partition reproducible
set.seed(123)
train_ind <- sample(seq_len(nrow(data)), size = smp_size)

train <- data[train_ind, ]
test <- data[-train_ind, ]

####
data.cor = cor(data[sapply(data, function(x) !is.factor(x))])

#install.packages("corrgram")
library(corrgram)
palette = colorRampPalette(c("green", "white", "red")) (20)
heatmap(x = data.cor, col = palette, symm = TRUE)

corrgram(data, order=TRUE, lower.panel=panel.shade,
         upper.panel=panel.pie, text.panel=panel.txt,
         main="Car Milage Data in PC2/PC1 Order")

#install.packages("corrplot")
library(corrplot)
corrplot(data.cor)

###
library(tree)

tree.model1 <- tree(Doctorate. ~ same.advisor. + highest.adv.tier + Honors. + RISE. + Cohort
                    + Class + Graduated. + num_yrs_enrolled + num_RD, train)
plot(tree.model1)
text(tree.model1,pretty =0, cex=0.8)

# with same topic in data set
#tree.model2 <- tree(Doctorate. ~ same.advisor. + highest.adv.tier + Honors. + RISE. + Cohort
                    + Class + Graduated. + num_yrs_enrolled + num_RD, train)
#plot(tree.model2)
#text(tree.model2,pretty =0, cex=0.8)

##############################################################################################

library(rpart)
fit <- rpart(Doctorate. ~ same.advisor. + highest.adv.tier + Honors. + RISE. + Cohort
             + Class + Graduated. + num_yrs_enrolled + num_RD, method = "class", data = train)

fit2 <- rpart(Doctorate. ~ same.advisor. + highest.adv.tier + Honors. + RISE. + Cohort
                    + Class + Graduated. + num_yrs_enrolled + num_RD + same.topic., method = "class", train)

printcp(fit) # display the results 
plotcp(fit) # visualize cross-validation results 
summary(fit) # detailed summary of splits

# plot tree 
plot(fit, uniform=TRUE, main="Classification Tree for Kyphosis")
text(fit, use.n=TRUE, all=TRUE, cex=.8)

plot(fit2, uniform=TRUE, main="Classification Tree for Kyphosis")
text(fit2, use.n=TRUE, all=TRUE, cex=.8)

#install.packages("rpart.plot")
library(rpart.plot)
rpart.plot(fit)
print(fit)

### Pruning?
ptree = prune.rpart(fit, fit$cptable[which.min(fit$ptable[,"xerror"]),"CP"])
rpart.plot(ptree)

#prune.rpart()
prune.DT = prune.tree(tree.model1,best = best.tree.size)
plot(prune.DT)
text(prune.DT,pretty =0)

#### Predict response

pred <- predict(fit, test, type="class")
#table(predict(fit, iris[-sub,], type = "class"), iris[-sub, "Species"])
length(pred)
length(test)
T <- table(pred, test$Doctorate.)
T

#install.packages("caret")
library(caret)
confusionMatrix(pred, test$Doctorate.)

#######################################################################################################
### Regression Models:
set.seed(1234)   #sets a seed

## bayesglm
#install.packages("arm")
library(arm)

bayes = bayesglm(Doctorate. ~ cnt_adv + same.advisor. + highest.adv.tier + Honors. + RISE. + Cohort
                 + Class + Graduated. + num_yrs_enrolled + num_RD, train, family = binomial("logit"))

summary(bayes)

bmodel = bayesglm(Doctorate. ~ 1, train, family = binomial("logit"))
summary(bmodel)

backwards = step(bayes)

forwards = step(bmodel,
                scope=list(lower=formula(bmodel),upper=formula(bayes)), direction="forward")

final_bayes = bayesglm(Doctorate. ~ highest.adv.tier + Honors. + RISE. + Class, train, family = binomial("logit"))
summary(final_bayes)

######################
## Regular old glm()
fullmod = glm(Doctorate. ~ cnt_adv + same.advisor. + highest.adv.tier + Honors. + RISE. + Cohort
              + Class + Graduated. + num_yrs_enrolled + num_RD, train, family = binomial("logit"), maxit=1000)
summary(fullmod)

nothing = glm(Doctorate. ~ 1, train, family = "binomial")
summary(nothing)

backwards = step(fullmod)

forwards = step(nothing,
                scope=list(lower=formula(nothing),upper=formula(fullmod)), direction="forward")

glm_model = glm(Doctorate. ~ Class + Honors. + highest.adv.tier + RISE., train, family = "binomial")

summary(glm_model)
anova(glm_model, fullmod, test ="Chisq")

#install.packages("lmtest")
library(lmtest)
lrtest(glm_model, fullmod)

### Pseudo R^2
#install.packages("pscl")
library(pscl)
pR2(glm_model) 
pR2(final_bayes)


### Variable Importance
#install.packages("varImp")
library(varImp)
varImp(final_bayes, scale = FALSE)
varImp(glm_model)


### Classification Rate
pred2 = predict(final_bayes, newdata=test)
accuracy <- table(pred2, test$Doctorate.)
sum(diag(accuracy))/sum(accuracy)

pred3 = predict(glm_model, newdata=test)
accuracy <- table(pred3, test$Doctorate.)
sum(diag(accuracy))/sum(accuracy)

###
# K-Fold Validation
ctrl <- trainControl(method = "repeatedcv", number = 10, savePredictions = TRUE)

mod_fit <- train(Doctorate. ~ Class + Honors. + highest.adv.tier + RISE.,  data=train, method="glm", family="binomial",
                 trControl = ctrl, tuneLength = 5)
pred4 = predict(mod_fit, newdata=test)
confusionMatrix(data=pred4, test$Doctorate.)
