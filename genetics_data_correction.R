
setwd("/Users/mandujanoreyes/Library/CloudStorage/GoogleDrive-juanipnc6@gmail.com/My Drive/PhD/JunZhu_WNS/Pest_resistance/genetics_data_correction")

covar1 = read.csv('CPB_temp_avgcovariance.csv', row.names = 1)
image(as.matrix(covar1))
image( as.matrix(covar1/rowSums(covar1)) )

covar2 = read.table("pcangsd_cpb_temp_cands.cov", header = FALSE, sep = "", dec = ".")
image(as.matrix(covar2))

covar = (covar1+covar2)/2
covar = covar1 #+covar2)/2
image(as.matrix(covar))

covar = covar2

meta = read.csv('CPB_temp_metadata.csv')

meta$Population

image(as.matrix(covar))


library(ggplot2)
library(dplyr)
library(readxl)

# Function for PCoA from covariance matrix
pcoa_from_covariance <- function(Sigma, groups, var_exp = 95.0) {
  n <- nrow(Sigma)
  
  # Convert covariance matrix to squared Euclidean distance matrix
  D2 <- outer(diag(Sigma), diag(Sigma), "+") - 2 * Sigma
  
  # Double centering to get the Gram matrix
  H <- diag(n) - matrix(1, n, n) / n
  G <- -0.5 * H %*% D2 %*% H
  
  # Perform eigenvalue decomposition
  eig <- eigen(G, symmetric = TRUE)
  
  # Retain only positive eigenvalues # maybe this is not necessary because they all are positive
  positive_eigenvalues <- eig$values > 0
  eig_vectors <- eig$vectors[, positive_eigenvalues]
  eig_values_sqrt <- sqrt(eig$values[positive_eigenvalues])
  
  # Compute principal coordinates
  PCoA_coords <- eig_vectors %*% diag(eig_values_sqrt)
  
  # Convert to data frame
  pcoa_df <- as.data.frame(PCoA_coords)
  colnames(pcoa_df) <- paste0("PC", 1:ncol(pcoa_df))
  pcoa_df_original = pcoa_df
  pcoa_df$Group <- groups  # Add group information
  
  # Compute group-level means
  group_means <- aggregate(. ~ Group, data = pcoa_df, FUN = mean)
  
  # Visualization
  plot <- ggplot(pcoa_df, aes(x = PC1, y = PC2, color = Group)) +
    geom_point(alpha = 0.7) +
    geom_point(data = group_means, aes(x = PC1, y = PC2), 
               shape = 21, fill = "black", size = 5, stroke = 1.5) +
    labs(title = "PCoA from Covariance Matrix", x = "PC1", y = "PC2") +
    theme_minimal()
  
  # Compute variance explained
  variance_explained <- eig$values[positive_eigenvalues] / sum(eig$values[positive_eigenvalues]) * 100
  
  # Create a data frame for Scree plotting
  scree_data <- data.frame(
    Principal_Component = seq_along(variance_explained),
    Variance_Explained = variance_explained,
    Cumulative_Variance_Explained = cumsum(variance_explained)
  ) 
  
  #th = c(scree_data$Principal_Component[scree_data$Cumulative_Variance_Explained >= var_exp])[1]
  #y_th = 2*max(scree_data$Variance_Explained)/3
  #lab_th = paste(var_exp,' % Variance explained')
  
  # Step 4: Plot the scree plot
  scree_plot <- ggplot(scree_data, aes(x = Principal_Component, y = Variance_Explained)) +
    geom_bar(stat = "identity", fill = "steelblue") +
    geom_line() +
    geom_point() +
    #geom_vline(xintercept = th, linetype="dotted", color = "red", size=1) +
    #geom_text(aes(x=th+2, label = lab_th, y = y_th), 
    #          colour="red", angle=90) +
    labs(
      title = "Scree Plot of PCoA",
      x = "Principal Coordinate",
      y = "Percentage of Variance Explained"
    ) +
    theme_minimal()
  
  return(list(coords = pcoa_df, plot2D = plot, scree_plot = scree_plot, group_means = group_means, coords_og = pcoa_df_original))
}

# test with iris datset
#data(iris)
#Sigma = cov(as.matrix(t( iris[,c(1,2,3,4)]))) 
#groups = iris$Species 

# our genetics data
Sigma = as.matrix(covar)
groups = meta$Population

# Run PCoA
result <- pcoa_from_covariance(Sigma, groups, var_exp = 30)

# Show the plots
print(result$plot2D)
print(result$scree_plot)

# result$coords

final_result = result$group_means[,c(1:11)]
final_result = final_result %>% left_join(unique(meta[,c(3,4,5)]), by = join_by(Group == Population))

locations_populatons_1 = read_excel('Table_Genomic_Samplesv2.xlsx', sheet = "Table_S#_WGS_Samples")

locations_populatons = locations_populatons_1 %>% dplyr::select(Year, Population, Latitude, Longitude) %>% unique()

final_result = final_result %>% left_join(locations_populatons, by=c("Group" = "Population")) %>% 
  dplyr::select(-Group.y, -Year.y) %>%
  rename(Pco1 = PC1, Pco2 = PC2, Pco3 = PC3, Pco4 = PC4, Pco5 = PC5, Pco6 = PC6,
         Pco7 = PC7, Pco8 = PC8, Pco9 = PC9, Pco10 = PC10, Year = Year.x) 


# write.csv(final_result, file = "/Users/mandujanoreyes/Documents/LocalPhD/Pest_Resistance_Data/new_genetics_Feb25.csv", row.names=FALSE)




# dim(result$coords_og)
better_genetics = cbind(meta[,c(2,3,4)], result$coords_og[,c(1:11)])

locations_populatons = locations_populatons_1 %>% dplyr::select(Year, Population, SampleID, Latitude, Longitude) # %>% unique()

better_genetics = better_genetics %>% left_join(locations_populatons, by=c("SampleID" = "SampleID")) %>% 
  dplyr::select(-Year.y, -Population.y) %>%
  rename(Pco1 = PC1, Pco2 = PC2, Pco3 = PC3, Pco4 = PC4, Pco5 = PC5, Pco6 = PC6,
         Pco7 = PC7, Pco8 = PC8, Pco9 = PC9, Pco10 = PC10, Year = Year.x, Population = Population.x) 


write.csv(better_genetics, file = "/Users/mandujanoreyes/Library/CloudStorage/GoogleDrive-juanipnc6@gmail.com/My Drive/PhD/JunZhu_WNS/Pest_resistance/Imputation/better_genetics_Jun2.csv", row.names=FALSE)
# write.csv(better_genetics, file = "/Users/mandujanoreyes/Library/CloudStorage/GoogleDrive-juanipnc6@gmail.com/My Drive/PhD/JunZhu_WNS/Pest_resistance/Imputation/better_genetics_Mar18.csv", row.names=FALSE)







