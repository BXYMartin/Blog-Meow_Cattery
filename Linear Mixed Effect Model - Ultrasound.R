library(glue)
library(lmerTest)
library(lattice)
library(sjPlot)
library(dplyr)

# Read the data from the CSV file
data <- read.csv('ultrasound.csv', sep=",")

# data <- data %>% 
#   filter(age_in_days < 5)

# Fit the multilevel model
model <- lmer(hd ~ days_before_delivery + (1 | id), data = data, REML=FALSE)

# # Extract standardized residuals
# resid_std <- resid(model, type="pearson") # if rstandard not available
# 
# # Identify outliers
# outliers <- abs(resid_std) > 70  # You can also try 3
# 
# # Remove outliers from the dataset
# data_clean <- data[!outliers, ]
# 
# # Refit the model
# model <- lmer(weight ~ age_in_days + birth_weight + hair_type + hair_color + month_of_birth + (1 | id), data = data_clean, REML=FALSE)

dotplot(ranef(model))

plot_model(model, terms = c("days_before_delivery", "(Intercept)"),
           show.values = TRUE, colors = c("blue", "red"), p.adjust.method = "bonferroni",
           title = "HD to age in days (adjusted p-values)")

tab_model(model, show.reflvl = TRUE)
# Extract the summary of the model
print(summary(model))

# Plot scatter
plot(data$days_before_delivery, data$weight)

# Compute residuals
plot(fitted(model), residuals(model))

# Plot residual histogram
hist(residuals(model))

# Plot Q-Q Plot
qqnorm(residuals(model))

null <- lmer(hd ~ (1 | id), data = data, REML=FALSE)

result <- anova(null, model)

print(result)