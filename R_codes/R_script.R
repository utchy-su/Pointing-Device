library('openxlsx')
library('effsize')

linear <- read.xlsx("path")
linear <- data.frame(linear)

nonlinear <- read.xlsx("path")
nonlinear <- data.frame(nonlinear)

print(linear)

num <- 19*14
mean_delta <- 3

data1 <- subset(linear$Throughput, linear$X1>=num)
print(data1)
data2 <- subset(nonlinear$Throughput, nonlinear$X1>=num)

lin_mean <- mean(data1)
lin_std <- sd(data1)

nl_mean <- mean(data2)
nl_std <- sd(data2)

print(paste("data length:",length(data1)))

plot_func <- function(lin_mean, lin_std, nl_mean, nl_std){
  x <- c(lin_mean, nl_mean)
  std <- c(lin_std, nl_std)
  
  colnames<- c("Linear", "Nonlinear")
  
  color <- c("blue", "orange")
  
  b <- barplot(x, ylim=c(0, max(x)+max(std)), ylab="AVC [pixels/ms]", names.arg=colnames,
               cex.names=2.0, cex.axis=1.0, cex.lab=2.0, col=color)
  
  arrows(b, x-std, b, x+std, code=3, lwd=1, angle=90, length=0.1)
}

# hist(linear$Time.Spent)
plot_func(lin_mean, lin_std, nl_mean, nl_std)

#equal variance?
result <- t.test(data1, data2, var.equal=FALSE)
power <- power.t.test(n=14*25-num, delta=mean_delta, sig.level=0.05, 
                      sd=lin_mean, type="two.sample", alternative="two.sided")
es <- cohen.d(data1, data2)

print(result)
print(power)
print(paste("delta: ", as.character(mean_delta/lin_mean)))
print(es)
