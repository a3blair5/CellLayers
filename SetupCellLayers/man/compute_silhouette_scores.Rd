% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/compute_silhouette_scores.R
\name{compute_silhouette_scores}
\alias{compute_silhouette_scores}
\title{Compute silhouette scores}
\usage{
compute_silhouette_scores(sobj, res_search, output_path)
}
\arguments{
\item{sobj}{A Seurat object}

\item{res_search}{A vector of type double that specifies the resolution parameters}

\item{output_path}{A character denoting the output path}
}
\value{
sil_df silhouette score summary statistics for each resolution's communities
}
\description{
Compute silhouette scores using the PCA embedding space (default 30 dimensions) for each resolution's communities.
}
