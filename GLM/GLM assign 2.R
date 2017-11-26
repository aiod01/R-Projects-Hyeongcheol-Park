
#Read Table and omit NA.
crime.dat <- read.table("~/Library/Mobile Documents/com~apple~CloudDocs/crime.dat.txt", header = T)
crime.dat<-na.omit(crime.dat)
attach(crime.dat)

# str(crime.dat)

#Full model test
fit1=lm(R~.,data=crime.dat)
summary(fit1)

#Variable selection by Stepwise
fit2 <- step(fit1, direction="both")
summary(fit2)

#Model selection ->fit2
anova(fit2, fit1)

#drop test->comparing AIC, drop M.
drop1(fit2, test="Chi")
fit3<-lm(R ~ Age + Ed + Ex0  + U1 + U2 + X, data=crime.dat)
summary(fit3)

#Checking correlation of two covariates.
#Check Multicollinearity by scatter plot.
#Multicollinearity searching out.
pairs(crime.dat)
cor(crime.dat)

#I figured out U1, U2 has corralation, so I deleted U1.
fit4<-lm(R ~ Age + Ed + Ex0  + U2 + X, data=crime.dat)
summary(fit4)

#Anova test and check which model is the best.
anova(fit4,fit3)

#Residual Plot and Normal QQ Plot.
plot(fitted(fit4), resid(fit4), main="Residual Plot",
     xlab="fitted value", ylab="residuals") 
abline(a=0,b=0)
qqnorm(resid(fit4))

# Log transformation to stabilize nonconstant variance.
fit4<-lm(log(R) ~ Age + Ed + Ex0  + U2 + X, data=crime.dat)
summary(fit4)
plot(fitted(fit4), resid(fit4), main="Residual Plot",
     xlab="fitted value", ylab="residuals") 
abline(a=0,b=0)
qqnorm(resid(fit4))

##################################Binomial Logit model.##################

# Nonconverging logit GLM
R1<-as.numeric(R>105)
fit1_bin<-glm(R1~.-R,family=binomial,data=crime.dat)
summary(fit1_bin)

# stepwise. But still nonconverging.
fit2_bin <- step(fit1_bin, direction="both")
summary(fit2_bin)

#Comparing AIC by drop1
drop1(fit2_bin, test = "Chisq")

#deleting U1 increase smallest AIC and cure multicollinearity between U1 and U2.
fit3_bin<-glm(R1 ~ Age + Ex1 + LF + NW + U2 + X,family=binomial,data=crime.dat)
summary(fit3_bin)

#Comparing AIC-> it seems if we drop one more covariate, AIC increase too much.
drop1(fit3_bin)# we keep this model.

#we check the dispersion parameter, By using quasibinomial.
fit4_bin_quasi<-glm(R1 ~ Age + Ex1 + LF + NW + U2 + X,family=quasibinomial,data=crime.dat)
summary(fit4_bin_quasi)#As quasibinimial's dispersion parameter is 0.4, we should use quasibinomial.
# we cannot say the assumptions for logit model hold well.

##################Poisson##################
# Change response variable.
R2<-round(R,digits=0)

#Full model-> many insignificant covariates exist.
fit1_poi<-glm(R2~.-R,family=poisson,data=crime.dat)
summary(fit1_poi)


# stepwise method for variable selection.
fit2_poi <- step(fit1_poi, direction="both")
summary(fit2_poi)#formula = R2 ~ Age + Ed + Ex0 + LF + U1 + U2 + W + X


drop1(fit2_poi)#AIC comparing- dropping LF increase very small amount of AIC.

#smaller model without LF, as the fit3 model.
fit3_poi<-glm(R2 ~ Age + Ed + Ex0 + U1 + U2 + W + X,family=poisson,data=crime.dat)
summary(fit3_poi) 

#ANOVA test of fit3_poi and fit2_poi
anova(fit3_poi,fit2_poi)# 4.2712 is the Deviance.
qchisq(0.95,1)  # qualtile of chisq is 3.84. 4.27>3.84. 
#So we reject the null hypothesis. we accept the model without LF.
drop1(fit3_poi)
fit4_poi<-glm(R2 ~ Age + Ed + Ex0 + U2 + W + X,family=poisson,data=crime.dat)
summary(fit4_poi) # tried a model without U1, as U1 increase AIC a little and has multicollinearity with U2.
drop1(fit4_poi)

anova(fit4_poi,fit3_poi)
qchisq(0.95,1)  # qualtile of chisq is 3.84. 14.8>3.84. So we reject the null. we accept the model
# without U1. we choose fit4_poi.


#Model diagnose:dispersion parameter 
fit4_poi_quasi<-glm(R2 ~ Age + Ed + Ex0+ U2+W + X,family=quasipoisson,data=crime.dat)
summary(fit4_poi_quasi)#Dispersion parameter for quasipoisson family taken to be 5.304443. 
#We cannot say that the assumptions for Poisson model hold well.

#For linear model R ~ Age + Ed + Ex0  + U2 + X,
#QuasibinomialR1 ~ Age + Ex1 + LF + NW + U2 + X,
#Quasipoisson R2 ~ Age + Ed + Ex0 +U2 + W + X

summary(fit4)
summary(fit4_bin_quasi)
summary(fit4_poi_quasi)

cor(Ex1, X)
