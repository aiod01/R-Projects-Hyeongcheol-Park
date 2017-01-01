#2.

n_1 <- 100000 # Prespecifed Sample size 
theta <- 1 # Prespecified mean of Poisson distribution 
eta <- exp(-theta) 

eps <- 0.01 # Prespecified value 

out_region <- numeric(20000) 

for (i in 1:20000){ 
  
  poisson_sample <- rpois(n = n_1, lambda = theta) 
  
  sample_sum <- sum(poisson_sample) 
  eta_hat <- (1 - 1/n_1)^(sample_sum) # The observed UMVUE for the parameter eta 
  
  out_region[i] <- (abs(eta_hat - eta) > eps) # Record whether the difference is larger than eps 
  
} 

# Calculate the simulation probability  

sum(out_region)/20000



#3




#4 
q4<-c(1.551, -1.170, -0.201, 1.143, 0.138, 3.103, 1.455, -2.121, -1.672, 6.150)
mean(q4)
q4-0.8376 


q4.1<-c(1.551, -0.201, 1.143, 0.138, 1.455 )
mean(q4.1)

q4-mean(q4.1)
q4.2<-c(1.551, -1.170, -0.201, 1.143, 0.138, 1.455 )
mean(q4.2)
q4-mean(q4.2)
#Hence, 0.486 is the estimator.