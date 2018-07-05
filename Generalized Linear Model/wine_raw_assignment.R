#read dataset.
wine <- read.csv(file="/Users/hyeongcheolpark/Library/Mobile Documents/com~apple~CloudDocs/UBC/2017-term1/538A GLM/winequality-red.csv", header=TRUE, sep=";")

# Understand data. Describe how the data is collected and what the data is.
View(wine)
head(wine)
str(wine)
summary(wine)
hist(wine$quality)
wine <- na.omit(wine)




# 3. Use summary statistics / exploratory data analysis to understand the data better or to identify 
#any obvious patterns. -> exploratory data analysis
cor(wine)
pairs(wine$quality)
wine_subset<-subset(wine, select = c(-free.sulfur.dioxide))
install.packages("PerformanceAnalytics")
library("PerformanceAnalytics")
my_data <- subset(wine, select=c(citric.acid, fixed.acidity,
total.sulfur.dioxide, free.sulfur.dioxide,density, pH))
chart.Correlation(my_data, histogram=TRUE, pch=15)
#alchole 0.47 volatile.acidity -0.39 for quality
#citric.acid, fixed.acidity0.67, 
# total.sulfur.dioxide, free.sulfur.dioxide  0.67, 
# density, fixed acidity 0.67, 
# pH fixed acidity -0.68


# 4. Choose an appropriate model and fit the model…  -> confirmatory data analysis

#Full model-> many insignificant covariates exist.
fit_poi<-glm(quality~.,family=poisson,data=wine_subset)
summary(fit_poi)

# stepwise method for variable selection.
fit_poi1 <- step(fit_poi, direction="both")
summary(fit_poi1)

anova(fit_poi1,fit_poi)
qchisq(0.95,7) # There is no difference between two model. So we choose smaller model.

drop1(fit_poi1)
# Based on common knowledge, the taste of wine is determined by compositions of many acid and other
#ingredients. The model is too small already so we stop dropping variables.


#sulphates: a wine additive which can contribute to sulfur dioxide gas (S02) levels, wich acts as an antimicrobial and antioxidant
#it makes sense that sulphates affects taste and quality of wine, as over 50ppm of S02 becomes evident in the nose and taste of wine.
#total sulfur dioxide: amount of free and bound forms of S02; in low concentrations, SO2 is mostly undetectable in wine,
#but at free SO2 concentrations over 50 ppm, SO2 becomes evident in the nose and taste of wine

fit_poi_quasi <- glm(quality ~ volatile.acidity + sulphates + alcohol, 
    family = quasipoisson, data = wine_subset)
summary(fit_poi_quasi)
cooks.distance(fit_poi_quasi)
which(cooks.distance(fit_poi_quasi)>1)

# Dispersion parameter for quasipoisson family taken to be 0.07654819
# It means that the model seriously violate the assumptions. Hence we use quasi poisson model with dispersion parameter 0.07.


#Linear model

fit_lm=lm(quality~.,data=wine_subset)
summary(fit_lm)

fit_lm2 <- step(fit_lm, direction="both")
summary(fit_lm2)

anova(fit_lm2,fit_lm)# smaller model is better.

drop1(fit_lm2)
#All negative value. AIC=2k−2ln(L). it means we don't need to delete any covariate. Also, Adjusted R
#square is too small. Hence we choose the current model.

#Residual Plot and Normal QQ Plot.
plot(fitted(fit_lm2), resid(fit_lm2), main="Residual Plot",
     xlab="fitted value", ylab="residuals") 
abline(a=0,b=0)
# Absolute clusting happened. It is obvious that regression is not proper for this dataset.
qqnorm(resid(fit4))

#binomial model
attach(wine_subset)
summary(wine$quality)
quality1<-as.numeric(quality>5.5)
str(quality1)
summary(quality1)
hist(quality1)
fit_bin<-glm(quality1~.-quality,family=binomial,data=wine_subset)
summary(fit_bin)

# stepwise. But still
fit2_bin <- step(fit_bin, direction="both")
summary(fit2_bin)

anova(fit2_bin,fit_bin)
qchisq(0.95,3)# we choose smaller model.

#Comparing AIC by drop1
drop1(fit2_bin, test = "Chisq")

#deleting chlorides increase smallest AIC.
fit3_bin<-glm(quality1 ~ fixed.acidity + volatile.acidity + citric.acid + 
                total.sulfur.dioxide + sulphates + alcohol,family=binomial,data=wine_subset)
summary(fit3_bin)

anova(fit3_bin,fit2_bin)
qchisq(0.95,1)# 5.32>3.841 It means there is difference between simpler model and complex model. 
#so we choose complex model.

#we check the dispersion parameter, By using quasibinomial.
fit4_bin_quasi<-glm(quality1 ~ fixed.acidity + volatile.acidity + citric.acid + 
                      chlorides + total.sulfur.dioxide + sulphates + alcohol,
                    family=quasibinomial,data=wine_subset)
summary(fit4_bin_quasi)#As quasibinimial's dispersion parameter is 1.14, 
#the assumptions for logit model hold well. We use logit model. But we need to check outlier, and Influential points.
cooks.distance(fit4_bin_quasi)
which(cooks.distance(fit4_bin_quasi)>1)
# There is no outlier in this data. So we keep the binomial model, with dispersion parameter 1.14

# 5. Interpret the results. -> results/discussions
# 6. Conclude.  -> conclusion
# 7. Now finish up intro and finally summary/abstract.