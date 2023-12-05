library(ggplot2)
library(tidyverse)
library(AER)
library(coefplot)
library(plm)
library(stargazer)

tdzsub=subset(data, tdz>1)
ntdzsub=subset(data, tdz==0)

# Graph treatment vs no treatment

avgtdz <- tdzsub %>%
  group_by(year) %>%
  summarise(tdz_sales=mean(tot_sales))

avgntdz <- ntdzsub %>%
  group_by(year) %>%
  summarise(ntdz_sales=mean(tot_sales))

merged_avg = merge(avgtdz, avgntdz, by="year", all=TRUE)

ggplot(merged_avg, aes(x = year)) + geom_line(aes(y = tdz_emp, color = "tdz"),
                                              linewidth=0.5)+ geom_line(aes(y = ntdz_emp,
                                              color="ntdz", size=0.5)) + labs(title =
                                              "averages of tdz vs non tdz",
                                              x="Year", y="avg tot_emp") + scale_color_manual(values=c("blue", "red"))

# Alt way to graph
avg_data <- tidyr::pivot_longer(merged_avg, cols = c("tdz_emp", "ntdz_emp"),,
                                names_to = "Variable", values_to = "Average")

ggplot(avg_data, aes(x = year, y = Average, color = Variable)) +
        geom_line() +
        labs(title = "Averages Over Time with Missing Values", x = "Year", y = "Average Value") +
        theme_minimal()

# Look for duplicated columns
data$id_year <- paste(data$idstd, data$year)
duplicate = duplicated(data$id_year)
subset(data, duplicate=="TRUE")

# convert data types for regression

data$time=ifelse(data$year > 2008, 1, 0)
data$treatdummy = data$time*data$tdz
data$year <- as_factor(data$year)
# data$tdz <- as_factor(data$tdz)
data$idstd <- as_factor(data$idstd)
data$email <- as_factor(data$email)
data$electricity <- as_factor(data$electricity)
data$website <- as_factor(data$website)

# Sales
sales$year <- as_factor(sales$year)
sales$idstd <- as_factor(sales$idstd)
sales$tdz <- as_factor(sales$tdz)
sales$email <- as_factor(sales$email)
sales$electricity <- as_factor(sales$electricity)
sales$website <- as_factor(sales$website)

slogit <- glm(tdz ~idstd +tot_emp+tot_sales+ email+website + electricity, data =sales , family = "binomial")

# credit pair
creditpair$year <- as_factor(creditpair$year)
creditpair$tdz <- as_factor(creditpair$tdz)
creditpair$idstd <- as_factor(creditpair$idstd)
creditpair$email <- as_factor(creditpair$email)
creditpair$electricity <- as_factor(creditpair$electricity)
creditpair$website <- as_factor(creditpair$website)

cplogit <- glm(tdz ~tot_emp+input_credit + lf_ed + electricity, data =creditpair , family = "binomial")

# Credit
credit$year <- as_factor(credit$year)
credit$tdz <- as_factor(credit$tdz)
credit$idstd <- as_factor(credit$idstd)
credit$email <- as_factor(credit$email)
credit$electricity <- as_factor(credit$electricity)
credit$website <- as_factor(credit$website)

clogit <- glm(tdz ~tot_emp+input_credit + electricity, data =credit, family = "binomial")
clogitmargin <- margins(clogit)
clogitmarginat <- margins(clogit, at=list(input_credit=50.16))
export_summs(clogit, clogitmargin, clogitmarginat, model.names=c("logit", "margin effect", "margin effect at mean input credit (50.16)"))

# lf_ed
education$year <- as_factor(education$year)
education$tdz <- as_factor(education$tdz)
education$idstd <- as_factor(education$idstd)
education$email <- as_factor(education$email)
education$electricity <- as_factor(education$electricity)
education$website <- as_factor(education$website)

elogit <- glm(tdz ~idstd +tot_emp+lf_ed +electricity, data =education , family = "binomial")

# sales pair
salespair$year <- as_factor(salespair$year)
salespair$tdz <- as_factor(salespair$tdz)
salespair$idstd <- as_factor(salespair$idstd)
salespair$email <- as_factor(salespair$email)
salespair$electricity <- as_factor(salespair$electricity)
salespair$website <- as_factor(salespair$website)

splogit <- glm(tdz ~tot_emp+lf_ed + tot_sales + electricity, data =salespair , family = "binomial")

# export_summs(slogit, splogitmargin, splogitmarginatmin, splogitmarginat1stq, splogitmarginatmedian, splogitmarginat3rd, splogitmarginatmax, model.names=c("logit", "marginal effects", "me at min", "me at 1st quartile", "me at median", "me at 3rd quartile", "me at max"))

# interaction between lf_ed and tot_emp

str(data)
logit <- glm(tdz ~idstd +tot_emp+log(tot_sales)+year+email+website + electricity, data =sales , family = "binomial")
# Convert data to panel data
pdata <- pdata.frame(data, index = c("idstd", "year"))

is.pbalanced(pdata)


# Run the actual regression, need tuning
# mod1 = lm(tot_emp~idstd + year + treatdummy, data=pdata)
mod1 = lm(tot_emp~idstd + year + tdz + tdz*time + time + time*email*website*electricity
          *credit, data=pdata)

# Robust standard error matrix
mod1_ro_se <- sqrt(diag(vcovHC(mod1, type="HC1")))

# Show the values of the matrix
stargazer(mod1, keep="treatdummy", type="text", se=list(mod1_ro_se),
          digits = 6, notes="HS Robust standard errors in parenthesis")






slogit <- glm(tdz ~tot_emp+tot_sales, data =sales , family = "binomial"(link="logit"))
slogitmargins=margins(slogit)
slogitmin=margins(slogit, at=list(tot_sales=2.773))
slogit1stq=margins(slogit, at=list(tot_sales=12.834))
slogitmedian=margins(slogit, at=list(tot_sales=14.369))
slogit3rd=margins(slogit, at=list(tot_sales=15.924))
slogitmax=margins(slogit, at=list(tot_sales=18.42))
export_summs(slogit, slogitmargins, slogitmin, slogit1stq, slogitmedian, slogit3rd, slogitmax, model.names=c("logit", "marginal effect", "margin at min", "at 1st quartile", "median", "3rd quartile", "max"))

clogit <- glm(tdz ~tot_emp+input_credit + input_credit:tot_emp, data =credit, family = "binomial"(link="logit"))
clogitmargin <- margins(clogit)
clogiitmarmin <- margins(clogit, at=list(input_credit=1))
clogiitmar1st <- margins(clogit, at=list(input_credit=30))
clogiitmarmedian <- margins(clogit, at=list(input_credit=50))
clogiitmar3rd <- margins(clogit, at=list(input_credit=70))
clogiitmarmax <- margins(clogit, at=list(input_credit=100))
export_summs(clogit, clogitmargin, clogiitmarmin, clogiitmar1st, clogiitmarmedian, clogiitmar3rd, clogiitmarmax, model.names=c("credit logit", "marginal effect", "marg at min", "1st q", "median", "3rd q", "max"))

elogit <- glm(tdz ~ tot_emp + lf_ed, data =education , family = "binomial")
emargins=margins(elogit)
summary(education)
emin=margins(elogit, at=list(tot_emp=5))
e1st=margins(elogit, at=list(tot_emp=16))
emedian=margins(elogit, at=list(tot_emp=38))
emin=margins(elogit, at=list(tot_emp=1))
emin=margins(elogit, at=list(lf_ed=1))
e1st=margins(elogit, at=list(tot_emp=5))
emedian=margins(elogit, at=list(tot_emp=15))
e3rd=margins(elogit, at=list(tot_emp=20))
emax=margins(elogit, at=list(tot_emp=100))
export_summs(elogit, emargins, emin, e1st, emedian, e3rd, emax, model.names=c("logit", "margial effect", "marginal effect at min", "1st quartile", "median", "3rd quartile", "max"))

cplogit <- glm(tdz ~tot_emp+input_credit + lf_ed + lf_ed:input_credit, data =creditpair , family = "binomial"(link="logit"))
cpmargin <- margins(cplogit)
cpmin <- margins(cplogit, at=list(input_credit=1))
cp1st <- margins(cplogit, at=list(input_credit=30))
cp2nd <- margins(cplogit, at=list(input_credit=50))
cp3rd <- margins(cplogit, at=list(input_credit=70))
cpmax <- margins(cplogit, at=list(input_credit=100))
export_summs(cplogit, cpmargin, cpmin, cp1st, cp2nd, cp3rd, cpmax, model.names=c("credit education logit", "marginal effects", "at min", "at 1st quartile","at median", "at 3rd quartile", "at max"))


splogit <- glm(tdz ~tot_emp+tot_sales + lf_ed + lf_ed:tot_sales, data =salespair , family = "binomial"(link="logit"))
spmargin <- margins(splogit)
spmin <- margins(splogit, at=list(tot_sales=1))
sp1st <- margins(splogit, at=list(tot_sales=30))
sp2nd <- margins(splogit, at=list(tot_sales=50))
sp3rd <- margins(splogit, at=list(tot_sales=70))
spmax <- margins(splogit, at=list(tot_sales=100))
export_summs(splogit, spmargin, spmin, sp1st, sp2nd, sp3rd, spmax, model.names=c("sales education logit", "marginal effects", "at min", "at 1st quartile","at median", "at 3rd quartile", "at max"))


