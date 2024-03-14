//! A Denoising model based on Linear Regression.

use smartcore::{
    linalg::basic::matrix::DenseMatrix,
    linear::linear_regression::{LinearRegression, LinearRegressionParameters},
};

/// A model for denoising time-series data based on linear regression.
pub struct LRModel {
    /// The linear regression model.
    models: Vec<LinearRegression<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>>,
    /// The number of elements in each window.
    window_size: usize,
}

impl
    super::Classical<
        LinearRegression<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>,
        LinearRegressionParameters,
    > for LRModel
{
    fn new(
        models: Vec<LinearRegression<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>>,
        window_size: usize,
    ) -> Self {
        Self {
            models,
            window_size,
        }
    }

    fn models(
        &self,
    ) -> &[LinearRegression<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>] {
        &self.models
    }

    fn window_size(&self) -> usize {
        self.window_size
    }
}
