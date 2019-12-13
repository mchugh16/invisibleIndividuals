# ===== GRAPH: Density Probability Predictions - Generated vs. Original =====

library(tidyverse)
library(ggplot2)
library(knitr)
library(reshape2)
library(haven)
library(scales)
library(extrafont)
loadfonts()

# -- Getting data
predictions <- read.csv("predictions_all.csv", header=TRUE)

# Converting columns to correct type
predictions$predicted_prob <- as.numeric(predictions$predicted_prob)
predictions$generated <- as.factor(predictions$generated)

# Years used for graph lables
labels_probs <- c("0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", "1")
labels_kdensity <- c("0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", "1")

png("prob_generated_density_plot2.png", units="in",width = 9, height = 6, res=1000)

# Generating graph
predictions %>%
  ggplot(aes(x = predicted_prob, y=stat(density/10), group=generated, color=generated, linetype=generated)) +
  geom_line(stat = "density", size=1) +
  scale_x_continuous(breaks=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0), 
                     labels = labels_probs) +
#   scale_y_continuous(breaks=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1),
#                       labels = labels_kdensity) +
  scale_linetype_manual(labels = c("Original", "Generated"), values=c("22", "solid")) +
  theme_minimal() + 
  scale_color_manual(labels = c("Original", "Generated"), values = c("dodgerblue3", "tomato3")) + 
  xlab("Classifier's Confidence in Gender Classification of Image (Probability)") +
  ylab("Proportion of Images") + 
  theme(panel.border = element_blank(), 
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_rect(fill = NA, color = NA),
        strip.background = element_rect(color=NA, fill=NA),
        axis.text.y=element_text(face="bold", size=8),
        plot.margin = margin(1, 1, 1, 1, "cm"),
        plot.title = element_text(hjust = 0.5, 
                                  size = 15, face = "bold"),
        legend.title = element_blank(),
        legend.spacing.x = unit(0.25, 'cm'),
        legend.position = "bottom",
        axis.line.x = element_line(colour="grey80"),
        axis.ticks.y = element_line(colour = "grey80"),
        axis.ticks.x = element_line(colour = "grey80"),                               
        axis.line.y = element_line(colour="grey80"),
        text = element_text(family="Avenir"),
        axis.text.x = element_text(face="bold", size=8))

dev.off()
