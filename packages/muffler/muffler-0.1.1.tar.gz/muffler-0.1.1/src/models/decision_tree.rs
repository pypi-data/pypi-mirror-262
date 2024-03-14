//! A Denoising model based on Linear Regression.

use smartcore::{
    linalg::basic::matrix::DenseMatrix,
    tree::decision_tree_regressor::{
        DecisionTreeRegressor, DecisionTreeRegressorParameters,
    },
};

/// A model for denoising time-series data based on linear regression.
pub struct DTModel {
    /// The linear regression model.
    models:
        Vec<DecisionTreeRegressor<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>>,
    /// The number of elements in each window.
    window_size: usize,
}

impl
    super::Classical<
        DecisionTreeRegressor<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>,
        DecisionTreeRegressorParameters,
    > for DTModel
{
    fn new(
        models: Vec<
            DecisionTreeRegressor<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>,
        >,
        window_size: usize,
    ) -> Self {
        Self {
            models,
            window_size,
        }
    }

    fn models(
        &self,
    ) -> &[DecisionTreeRegressor<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>]
    {
        &self.models
    }

    fn window_size(&self) -> usize {
        self.window_size
    }
}
