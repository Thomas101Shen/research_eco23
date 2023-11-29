library(ggplot2)
library(tidyverse)
library(AER)
library(coefplot)
library(plm)
library(stargazer)

tdzsub=subset(no_dropouts0513, tdz==1)
ntdzsub=subset(no_dropouts0513, tdz==0)

tdzsub=subset(no_dropouts0513, tdz==1)
ntdzsub=subset(no_dropouts0513, tdz==0)

avgtdz <- tdzsub %>%
  group_by(year) %>%
  summarise(tdz_emp=mean(tot_emp))

avgntdz <- ntdzsub %>%
  group_by(year) %>%
  summarise(ntdz_emp=mean(tot_emp))

merged_avg = merge(avgtdz, avgntdz, by="year", all=TRUE)

ggplot(merged_avg, aes(x = year)) + geom_line(aes(y = tdz_emp, color = "tdz"),
                                    linewidth=1)+ geom_line(aes(y = ntdz_emp,
                                    color="ntdz", linewidth=1)) + labs(title =
                                    "averages of tdz vs non tdz",
                                    x="Year", y="avg tot_emp")+
                                    scale_color_manual(values=c("blue", "red"))

no_dropouts0513$time=ifelse(no_dropouts0513$year > 2008, 1, 0)
no_dropouts0513$treatdummy = no_dropouts0513$time*no_dropouts0513$tdz
no_dropouts0513$year <- as_factor(no_dropouts0513$year)
no_dropouts0513$tdz <- as_factor(no_dropouts0513$tdz)
levels(no_dropouts0513$tdz) <- c("control", "treated")
no_dropouts0513$idstd <- as_factor(no_dropouts0513$idstd)

str(no_dropouts0513)

no_dropouts0513$id_year <- paste(no_dropouts0513$idstd, no_dropouts0513$year)
duplicate = duplicated(no_dropouts0513$id_year)
subset(no_dropouts0513, duplicate=="TRUE")

pdata <- pdata.frame(no_dropouts0513, index = c("idstd", "year"))

is.pbalanced(pdata)


# mod1 = lm(tot_emp~idstd + year + treatdummy, data=pdata)
mod1 = lm(tot_emp~idstd + year + tdz +tdz*time + time + E-mail*website*electricity
          *credit, data=pdata)
mod1_ro_se <- sqrt(diag(vcovHC(mod1, type="HC1")))

stargazer(mod1, keep="treatdummy", type="text", se=list(mod1_ro_se),
          digits = 6, notes="HS Robust standard errors in parenthesis")